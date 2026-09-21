#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2042: one poller for both status channels.

A BIOS push reports free-text progress - "node001: 2 stage(s), 7 setting(s) to
apply" - on the generic status channel. The control channel next to it parses
every message as node:command result:message, so the daemon raises on a line that
is not that shape and answers 500; the CLI then stops streaming and the operator
sees "Something Went Wrong 500" instead of the push.

There is deliberately one function rather than one per channel. The caller says
which channel its own work writes to; the reply says which renderer to use.
"""

import json
import logging

import pytest

import luna.utils.log as luna_log
from luna.utils.helper import Helper


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

    def __bool__(self):
        # requests.Response is falsy for any code outside 2xx. A fake without
        # this is truthy at 404 and hides a poller that never stops.
        return self.status_code < 400

    def json(self):
        return self.payload


@pytest.fixture
def polled(monkeypatch):
    """Serves a scripted list of replies and records every route asked for."""
    import luna.utils.helper as helper_module
    asked = []
    replies = []

    def get_raw(self, route=None, uri=None, noexit=False):
        asked.append(route)
        if len(asked) > 5000:
            # a poller that never stops would otherwise hang the suite instead
            # of failing it, and this file exists to catch exactly that
            raise AssertionError(f'poller did not stop after {len(asked)} requests')
        return replies.pop(0) if replies else FakeResponse(404, {})

    monkeypatch.setattr(helper_module.Rest, 'get_raw', get_raw)
    monkeypatch.setattr(helper_module, 'sleep', lambda _seconds: None)
    return {'asked': asked, 'replies': replies}


def lines(content, status=200):
    return FakeResponse(200, {'message': ';;'.join(content), 'status': status})


def test_a_plain_line_channel_is_read_from_config_not_control(polled, capsys):
    """
    The bug: bios asked control/status, whose parser cannot read its lines. The
    route is the caller's to choose, and bios chooses the generic one.
    """
    polled['replies'].append(lines(['12:00:00 :: node001: 2 stage(s) to apply']))
    Helper().dig_status('req-1', 1, 'bios', route='config')
    assert polled['asked'][0] == 'config/status/req-1'
    assert 'control' not in polled['asked'][0]


def test_the_control_callers_still_read_the_control_channel(polled):
    """The three existing callers must not have moved channel."""
    polled['replies'].append(FakeResponse(200, {'control': {'power': {'ok': {}, 'on': {}, 'off': {}},
                                                            'failed': {}}}))
    Helper().dig_status('req-2', 1, 'power')
    assert polled['asked'][0] == 'control/status/req-2'


def test_plain_lines_are_printed_rather_than_handed_to_control_print(polled, capsys):
    """
    control_print reads content['control'][system]; a generic reply has no such
    key, so routing one into it prints nothing at all - silently.
    """
    polled['replies'].append(lines(['12:00:00 :: node001: applied',
                                    '12:00:02 :: node001: 1 stage(s) applied']))
    Helper().dig_status('req-3', 1, 'bios', route='config')
    printed = capsys.readouterr().out
    assert 'node001: applied' in printed
    assert 'node001: 1 stage(s) applied' in printed


def test_the_renderer_follows_the_reply_not_the_named_channel(polled, capsys):
    """
    A caller naming a channel cannot pick the wrong printer: the reply's shape
    decides. A control-shaped reply renders as the node table whatever was asked.
    """
    polled['replies'].append(FakeResponse(200, {'control': {'power': {'ok': {'node001': 'power on'},
                                                                     'on': {}, 'off': {}},
                                                            'failed': {}}}))
    Helper().dig_status('req-4', 1, 'power')
    printed = capsys.readouterr().out
    assert 'node001' in printed and 'Node Name' in printed


def test_a_failing_line_is_reported_and_the_outcome_is_false(polled, capsys):
    polled['replies'].append(lines(['12:00:00 :: node001: refused'], status=500))
    assert Helper().dig_status('req-5', 1, 'bios', route='config') is False
    assert 'FAILED' in capsys.readouterr().out


def test_a_clean_run_returns_true_so_the_caller_can_close_the_stream(polled):
    polled['replies'].append(lines(['12:00:00 :: node001: applied']))
    assert Helper().dig_status('req-6', 1, 'bios', route='config') is True


def test_the_stream_ends_on_404_rather_than_polling_forever(polled):
    polled['replies'].extend([lines(['12:00:00 :: a']), lines(['12:00:01 :: b'])])
    Helper().dig_status('req-7', 1, 'bios', route='config')
    assert len(polled['asked']) == 3   # two message replies, then the 404


def test_polling_does_not_recurse(polled):
    """
    A BIOS push polls every two seconds across reboots. As a recursion that is a
    frame per poll, and a long push would exhaust the stack rather than finish.
    """
    polled['replies'].extend([lines([f'12:00:00 :: line {n}']) for n in range(2000)])
    Helper().dig_status('req-8', 1, 'bios', route='config')
    assert len(polled['asked']) == 2001


def test_bios_push_reads_the_generic_channel(monkeypatch):
    """
    The caller-level pin. This is the defect: bios_push named the control channel,
    whose daemon-side parser raises on a line without the node:command shape, and
    answers 500 - so the operator saw "Something Went Wrong 500" and no push.
    """
    import luna.biosconfig as biosconfig
    asked = {}

    monkeypatch.setattr(biosconfig.Rest, 'post_raw',
                        lambda self, route, payload: FakeResponse(200, {'message': 'queued',
                                                                       'request_id': 'req-9'}))
    monkeypatch.setattr(biosconfig.Helper, 'dig_status',
                        lambda self, request_id, count, system, route='control':
                        asked.update({'route': route, 'system': system}) or True)

    biosconfig.bios_push('node', {'name': 'node001', 'biosconfig': 'golden'})
    assert asked == {'route': 'config', 'system': 'bios'}


def test_a_later_good_line_is_not_marked_failed_by_an_earlier_bad_one(polled, capsys):
    """
    The marker is per batch. A push whose first node refuses and whose second
    succeeds must not report the second as a failure - while the overall outcome
    still comes back False.
    """
    polled['replies'].append(lines(['12:00:00 :: node002: refused'], status=500))
    polled['replies'].append(lines(['12:00:04 :: node003: applied']))
    assert Helper().dig_status('req-10', 1, 'bios', route='config') is False
    printed = capsys.readouterr().out
    assert '[FAILED] 12:00:00 :: node002: refused' in printed
    assert '[======] 12:00:04 :: node003: applied' in printed


def test_a_failed_push_exits_non_zero(monkeypatch, capsys):
    """
    A push that reported failures has to be detectable by a script, not only
    readable by whoever watched it. Same signal the osimage pack and clone
    paths give for the same reason.
    """
    import luna.biosconfig as biosconfig
    monkeypatch.setattr(biosconfig.Rest, 'post_raw',
                        lambda self, route, payload: FakeResponse(200, {'message': 'queued',
                                                                       'request_id': 'req-11'}))
    monkeypatch.setattr(biosconfig.Helper, 'dig_status',
                        lambda self, *a, **k: False)

    with pytest.raises(SystemExit) as exited:
        biosconfig.bios_push('node', {'name': 'node001', 'biosconfig': 'golden'})
    assert exited.value.code == 1
    assert 'FAILED' in capsys.readouterr().err


def test_a_clean_push_does_not_exit(monkeypatch):
    """The other half: success must not become an exit."""
    import luna.biosconfig as biosconfig
    monkeypatch.setattr(biosconfig.Rest, 'post_raw',
                        lambda self, route, payload: FakeResponse(200, {'message': 'queued',
                                                                       'request_id': 'req-12'}))
    monkeypatch.setattr(biosconfig.Helper, 'dig_status', lambda self, *a, **k: True)
    assert biosconfig.bios_push('node', {'name': 'node001', 'biosconfig': 'golden'}) is not None
