#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2356: osimage create follows its build through the shared poller.

The CLI carries seven hand-written status-polling closures, each a copy of the one
beside it, and a bug fixed in one does not reach the other six. A verb that needs
to follow a status stream uses Helper().dig_status; the list below is the allowlist
that says which closures predate it, with the reason each is still there.

Extracting the seven is a separate change and deliberately not this one's, so the
rule is pinned without touching them: nothing may join the list.
"""

import ast
import json
import logging
import os
import types

import pytest

import luna.utils.log as luna_log
from luna.utils.helper import Helper


LUNA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'luna')

# {(module, the function holding the closure): why it is still a closure}
INLINE_POLLERS = {
    ('osimage.py', 'pack_osimage'):
        'the original. Every closure below is a copy of this one',
    ('osimage.py', 'clone_osimage'):
        'copied from pack: a clone that is not bare packs, and follows that chain',
    ('osimage.py', 'updatecerts_osimage'):
        'copied from pack: the cert refresh repacks the image',
    ('osimage.py', 'kernel_osimage'):
        'copied from pack: a kernel change repacks the image',
    ('service.py', 'service_action'):
        'copied from pack, onto a third channel - it polls service/status',
    ('utils/helper.py', 'grab_osimage'):
        'copied from pack: an osgrab packs what it grabbed',
    ('utils/helper.py', 'push_osimage'):
        'copied from pack: an ospush packs what it pushed',
}


@pytest.fixture(autouse=True)
def _stub_logger():
    """
    A logger without Log.init_log()'s root-only file handler.
    """
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _strings(node):
    return [found.value for found in ast.walk(node)
            if isinstance(found, ast.Constant) and isinstance(found.value, str)]


def _polling_closures(path):
    """
    The functions in one module that hold a nested status-polling closure: an inner
    function calling get_raw, inside a function that builds a
    '<channel>/status/<request_id>' uri. Keyed on that shape and not on a name, so
    a copy called anything at all is caught.
    """
    with open(path, 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    holders = set()
    for outer in ast.walk(tree):
        if not isinstance(outer, ast.FunctionDef):
            continue
        if not any('/status/' in text for text in _strings(outer)):
            continue
        for inner in ast.walk(outer):
            if inner is outer or not isinstance(inner, ast.FunctionDef):
                continue
            if any(isinstance(call.func, ast.Attribute) and call.func.attr == 'get_raw'
                   for call in ast.walk(inner) if isinstance(call, ast.Call)):
                holders.add(outer.name)
    return holders


def _modules():
    for root, dirs, files in os.walk(LUNA):
        dirs[:] = [directory for directory in dirs if directory != '__pycache__']
        for name in sorted(files):
            if name.endswith('.py'):
                path = os.path.join(root, name)
                yield os.path.relpath(path, LUNA), path


def test_no_eighth_inline_status_poller_is_written():
    """
    One shared poller, and an allowlist of the copies that predate it.
    """
    found = {(module, holder)
             for module, path in _modules() for holder in _polling_closures(path)}
    extra = sorted(found - set(INLINE_POLLERS))
    assert not extra, (
        f'{extra} poll a status stream with their own closure.\n'
        'Use Helper().dig_status(request_id, 1, route=...) instead - there are already '
        'seven copies of that closure and a fix in one reaches none of the others.\n'
        'If a closure is genuinely unavoidable, add it to INLINE_POLLERS with the reason.')


def test_the_allowlist_names_closures_that_still_exist():
    """
    An entry left behind after a closure is extracted hides the next copy, because
    the name is already excused.
    """
    found = {(module, holder)
             for module, path in _modules() for holder in _polling_closures(path)}
    gone = sorted(set(INLINE_POLLERS) - found)
    assert not gone, (
        f'{gone} no longer hold a polling closure. Delete their INLINE_POLLERS entries, '
        'or the name stays excused for whatever is written there next.')


def _answer(code, payload):
    """
    A daemon answer. payload None is a bodyless answer, which is not hypothetical:
    get_access_code turns a message containing 'updated', 'removed' or 'deleted'
    into a 204 with no body, and a body is where the request_id lives.
    """
    content = b'' if payload is None else json.dumps(payload).encode()
    return types.SimpleNamespace(status_code=code, content=content,
                                 json=lambda: json.loads(content))


@pytest.fixture
def daemon(monkeypatch):
    """
    The _create route, the record it needs, and the poller, all faked at the module
    luna/osimage.py imports them into.
    """
    import luna.osimage as osimage_module
    state = {'answer': _answer(200, {'message': 'osimage creation for compute queued',
                                     'request_id': 'R1'}),
             'added': [], 'asked': [], 'followed': None, 'outcome': True}

    class Rest():
        def __init__(self):
            pass

        def get_raw(self, route=None, uri=None, noexit=False, timeout=None):
            state['asked'].append(route)
            return state['answer']

    def add_record(self, table=None, data=None):
        state['added'].append((table, data['name']))
        return True

    def dig_status(self, request_id=None, count=None, system=None, route='control'):
        state['followed'] = (request_id, route)
        return state['outcome']

    monkeypatch.setattr(osimage_module, 'Rest', Rest)
    monkeypatch.setattr(Helper, 'add_record', add_record)
    monkeypatch.setattr(Helper, 'dig_status', dig_status)
    state['create'] = lambda: osimage_module.OSImage(
        args={'command': 'osimage', 'action': 'create', 'name': 'compute'})
    return state


def test_a_create_makes_the_record_and_follows_the_generic_channel(daemon, capsys):
    """
    The record through the path add uses, then one call to _create, then the shared
    poller on the generic channel - a build reports free-text progress, which the
    control channel's parser cannot read.
    """
    daemon['create']()
    out = capsys.readouterr()
    assert daemon['added'] == [('osimage', 'compute')]
    assert daemon['asked'] == ['config/osimage/compute/_create']
    assert daemon['followed'] == ('R1', 'config')
    assert 'Image compute created' in out.out and 'FAILED' not in out.out + out.err


def test_a_deduplicated_create_follows_the_earlier_build(daemon, capsys):
    """
    A create for an image already queued is answered with the earlier create's
    request_id, not an error. Following that stream is the point: both operators
    watch the one build.
    """
    daemon['answer'] = _answer(200, {'message': 'osimage creation for compute already queued',
                                     'request_id': 'R0'})
    daemon['create']()
    out = capsys.readouterr()
    assert daemon['followed'] == ('R0', 'config')
    assert 'already queued' in out.out
    assert 'FAILED' not in out.out + out.err


def test_an_answer_with_no_body_fails_rather_than_claiming_success(daemon, capsys):
    """
    No body means no request_id, and the build's outcome lives only on that stream.
    Saying so and exiting beats reporting a create nobody can follow.
    """
    daemon['answer'] = _answer(200, None)
    with pytest.raises(SystemExit):
        daemon['create']()
    assert daemon['followed'] is None
    assert 'no build was queued' in capsys.readouterr().err


def test_a_refused_create_reports_the_daemons_reason(daemon, capsys):
    """
    The route refuses an image that is not there, and the operator reads why.
    """
    daemon['answer'] = _answer(404, {'message': 'OS image compute does not exist'})
    with pytest.raises(SystemExit):
        daemon['create']()
    assert daemon['followed'] is None
    assert 'does not exist' in capsys.readouterr().err


def test_a_build_that_reported_failures_exits_non_zero(daemon, capsys):
    """
    dig_status returns whether everything it saw succeeded, so a script can tell a
    failed build from a watched one.
    """
    daemon['outcome'] = False
    with pytest.raises(SystemExit):
        daemon['create']()
    assert '[ FAILED ]' in capsys.readouterr().err
