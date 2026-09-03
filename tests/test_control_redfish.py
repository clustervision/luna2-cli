#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-1998: what `luna control redfish` actually sends, and what it shows back.

Before this, the file given with -f was read, printed to the terminal between two
"Under Development" banners, and thrown away. The single-node path was a GET, so
there was no transport for a body on either path. Both halves are pinned here.
"""

import base64
import io
import json
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse():
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.payload = payload if payload is not None else {}
        self.content = json.dumps(self.payload).encode()

    def json(self):
        return self.payload


@pytest.fixture
def sent(monkeypatch):
    """Captures what the CLI posts, without a daemon behind it."""
    posted = []

    import luna.control as control

    def fake_post_raw(self, uri, payload):
        posted.append({'uri': uri, 'payload': payload})
        return FakeResponse(payload={'request_id': None,
                                     'control': {'redfish': {'ok': {}}, 'failed': {}}})

    monkeypatch.setattr(control.Rest, 'post_raw', fake_post_raw, raising=False)
    # the spinner forks a process; not wanted in a test
    monkeypatch.setattr(control, 'Process', lambda *a, **k: type(
        'NoProcess', (), {'start': lambda s: None, 'terminate': lambda s: None})())
    monkeypatch.setattr(control.Helper, 'control_print', lambda self, *a, **k: 1)
    return posted


def control_with(args):
    """A Control instance driven straight at action_status, as the CLI does."""
    from luna.control import Control
    instance = Control.__new__(Control)
    instance.logger = luna_log.Log.get_logger()
    instance.args = args
    instance.route = 'control'
    return instance


def redfish_args(action='setting', node='node001', uri='/redfish/v1/Systems/1/Bios',
                 content='{"BootMode": "Uefi"}'):
    return {
        'system': 'redfish',
        'action': action,
        'node': node,
        'uri': uri,
        'file': io.StringIO(content) if content is not None else None,
    }


# --- the payload actually leaves -------------------------------------------

def test_the_file_is_sent_rather_than_printed(sent, capsys):
    """
    The whole defect: action_status read the file, printed it between two banners
    and discarded it. An operator's file contents have no business on the terminal,
    and a banner is not an implementation.
    """
    control_with(redfish_args()).action_status()
    assert len(sent) == 1
    body = sent[0]['payload']['control']['redfish']['setting']
    assert base64.b64decode(body['content']).decode() == '{"BootMode": "Uefi"}'
    printed = capsys.readouterr().out
    assert 'Under Development' not in printed
    assert 'BootMode' not in printed


def test_the_content_travels_base64():
    """
    The daemon strips ' and " out of every string in a request body, so raw JSON
    would arrive as {BootMode: Uefi} and fail to parse. This is the same convention
    the script fields already use.
    """
    encoded = base64.b64encode('{"BootMode": "Uefi"}'.encode()).decode()
    assert '"' not in encoded and "'" not in encoded


def test_a_single_node_still_uses_the_hostlist_form(sent):
    """
    Redfish carries a body and the single-node control route is a GET, so there is
    only one route that can take it. Using it for one node too is what keeps power,
    sel and chassis on the path they have always used.
    """
    control_with(redfish_args(node='node001')).action_status()
    assert sent[0]['uri'] == 'control/action/redfish/_setting'
    assert sent[0]['payload']['control']['redfish']['setting']['hostlist'] == 'node001'


def test_a_hostlist_goes_through_unexpanded(sent):
    """The daemon expands it; sending it expanded would put 4000 names in a URL body."""
    control_with(redfish_args(node='node[001-010]')).action_status()
    assert sent[0]['payload']['control']['redfish']['setting']['hostlist'] == 'node[001-010]'


def test_the_uri_reaches_the_daemon(sent):
    control_with(redfish_args(uri='/redfish/v1/Managers/1')).action_status()
    assert sent[0]['payload']['control']['redfish']['setting']['uri'] == '/redfish/v1/Managers/1'


def test_upload_posts_under_its_own_action(sent):
    control_with(redfish_args(action='upload')).action_status()
    assert sent[0]['uri'] == 'control/action/redfish/_upload'
    assert 'upload' in sent[0]['payload']['control']['redfish']


# --- refusing readably, before the network ---------------------------------

def test_a_missing_uri_is_refused_with_the_flag_that_fixes_it(sent, capsys):
    control_with(redfish_args(uri=None)).action_status()
    assert not sent
    # an error belongs on stderr, so a caller redirecting stdout still sees it
    assert '-U/--uri' in capsys.readouterr().err


def test_a_missing_file_is_refused_with_the_flag_that_fixes_it(sent, capsys):
    control_with(redfish_args(content=None)).action_status()
    assert not sent
    assert '-f/--file' in capsys.readouterr().err


# --- the other subsystems are untouched ------------------------------------

@pytest.mark.parametrize('system,action', [
    ('power', 'status'), ('sel', 'list'), ('chassis', 'identify'),
])
def test_power_sel_and_chassis_keep_the_single_node_get(monkeypatch, system, action):
    """
    A regression floor. These three have used the single-node GET route since 2023,
    and the redfish branch must not have moved them onto the hostlist path.
    """
    import luna.control as control

    asked = []
    monkeypatch.setattr(control.Rest, 'get_raw',
                        lambda self, uri, timeout=None: asked.append(uri) or FakeResponse(payload={}),
                        raising=False)
    monkeypatch.setattr(control.Presenter, 'show_table_col',
                        lambda self, *a, **k: True, raising=False)
    control_with({'system': system, 'action': action, 'node': 'node001'}).action_status()
    assert asked == [f'control/action/{system}/node001/_{action}']


# --- nextboot: a slow BMC must not turn a reset into a reported timeout ----

def test_a_single_node_control_action_waits_longer_than_a_lookup(monkeypatch):
    """
    Arming the boot override and resetting is several Redfish round trips, about
    18 s on an AMI board, against the 20 s every other request gets. The daemon
    bounds each BMC call itself, so a longer wait costs nothing on a dead BMC and
    stops a slow one from reporting failure for a node already rebooting.
    """
    import luna.control as control
    asked = []
    monkeypatch.setattr(control.Rest, 'get_raw',
                        lambda self, uri, timeout=None: asked.append((uri, timeout))
                        or FakeResponse(payload={}), raising=False)
    monkeypatch.setattr(control.Presenter, 'show_table_col',
                        lambda self, *a, **k: True, raising=False)
    control_with({'system': 'nextboot', 'action': 'bios', 'node': 'node001'}).action_status()
    assert asked == [('control/action/nextboot/node001/_bios', control.Control.action_timeout)]
    assert control.Control.action_timeout > 20


def test_the_rest_layer_uses_the_caller_timeout_only_when_given(monkeypatch):
    from luna.utils import rest
    seen = []

    class FakeSession():
        def get(self, url, **kwargs):
            seen.append(kwargs.get('timeout'))
            return FakeResponse(payload={})
    instance = rest.Rest.__new__(rest.Rest)
    instance.logger = luna_log.Log.get_logger()
    instance.daemon = 'https://daemon:7050'
    instance.security = False
    instance.request_timeout = 20
    instance.session = FakeSession()
    monkeypatch.setattr(rest.Rest, 'get_token', lambda self: 'token', raising=False)
    instance.get_raw('control/action/power/node001/_status')
    instance.get_raw('control/action/nextboot/node001/_bios', timeout=60)
    assert seen == [20, 60]


# --- what the operator is shown --------------------------------------------

def response_with(system='redfish', ok=None):
    return {'control': {system: {'ok': ok or {}, 'on': {}, 'off': {}}, 'failed': {}}}


def test_a_redfish_success_reports_what_it_did(capsys):
    """
    control_print prints the case name for a success, so every redfish node would
    say 'OK' and the operator would never learn which resource the setting was
    staged on. That is the one thing they asked for.
    """
    from luna.utils.helper import Helper

    Helper().control_print('redfish', response_with(
        ok={'node001': 'staged on /redfish/v1/Systems/1/Bios/Settings, applies OnReset'}), 1)
    assert 'Bios/Settings' in capsys.readouterr().out


def test_a_power_success_still_reports_ok(capsys):
    """The other half of the same change: power output is byte-identical to before."""
    from luna.utils.helper import Helper

    Helper().control_print('power', response_with(system='power', ok={'node001': 'power on'}), 1)
    printed = capsys.readouterr().out
    assert 'OK' in printed and 'power on' not in printed


def test_a_failure_still_reports_the_reason(capsys):
    from luna.utils.helper import Helper

    content = {'control': {'redfish': {'ok': {}, 'on': {}, 'off': {}},
                           'failed': {'node002': '192.0.2.10: connect timeout'}}}
    Helper().control_print('redfish', content, 1)
    assert 'connect timeout' in capsys.readouterr().out
