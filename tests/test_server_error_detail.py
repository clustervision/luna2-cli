#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2212: handle a daemon 500 at the shared REST boundary, before a command can
discard its reason. Message renders the compact reason on its own indented line.

Real request methods use a fake HTTP session. Raw calls, decoded calls, login,
validation and followers all stop on the same error. Malformed bodies fall back
to Server Error, followers close their progress processes, and other HTTP codes
and job statuses keep their existing meanings.
"""

import json
import logging
import types

import pytest
import requests

from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.message import Message
from luna.utils.rest import Rest


DETAIL = "TypeError: unsupported operand type(s) for +: 'NoneType' and 'list' (utils/model.py:105)"
BODY = {'message': 'Server Error', 'detail': DETAIL}
RENDERED = f'HTTP ERROR :: 500 Server Error\n    {DETAIL}\n'


@pytest.fixture(autouse=True)
def logger(monkeypatch):
    """
    Keep test logging independent of the controller's log files.
    """
    monkeypatch.setattr(Log, '_Log__logger', logging.getLogger('luna2-cli-tests'))


def answer(body=BODY, code=500):
    """
    A real requests.Response, including the falsy truth value of an HTTP 500.
    """
    response = requests.Response()
    response.status_code = code
    response._content = json.dumps(body).encode()
    return response


def install_session(monkeypatch, request):
    """
    Replace only credentials and HTTP transport; run the real REST methods.
    """
    def initialize(self):
        self.logger = logging.getLogger('luna2-cli-tests')
        self.daemon = 'https://daemon'
        self.username, self.password = 'user', 'password'
        self.request_timeout, self.security = 20, False
        self.session = types.SimpleNamespace(get=request, post=request)

    monkeypatch.setattr(Rest, '__init__', initialize)
    monkeypatch.setattr(Rest, 'get_token', lambda self: 'cached-token')


# --------------------------------------------------------- request paths ----

@pytest.mark.parametrize('method', [
    'get_data', 'post_data', 'get_delete', 'post_clone', 'get_status', 'get_raw', 'post_raw',
])
def test_every_request_path_reports_500_before_returning_to_the_command(monkeypatch, capsys, method):
    """
    A command never receives a 500 to decode, replace or accidentally ignore.
    """
    calls = []

    def request(url, **kwargs):
        calls.append(url)
        return answer()

    install_session(monkeypatch, request)
    with pytest.raises(SystemExit) as exited:
        getattr(Rest(), method)('node')
    assert exited.value.code == 1
    assert len(calls) == 1
    printed = capsys.readouterr()
    assert printed.err == RENDERED
    assert printed.out == ''


@pytest.mark.parametrize('parser', [False, True])
def test_the_daemon_probe_uses_the_same_500_check(monkeypatch, capsys, parser):
    """
    Parser construction and command validation both call the version probe.
    """
    install_session(monkeypatch, lambda *a, **k: answer())
    monkeypatch.setattr('luna.utils.rest.requests.get', lambda *a, **k: answer())
    with pytest.raises(SystemExit):
        Rest().daemon_validation(parser=parser)
    assert capsys.readouterr().err == RENDERED


def test_token_failure_uses_the_same_500_check(monkeypatch, capsys):
    """
    Login checks the response before attempting to read or store a token.
    """
    install_session(monkeypatch, lambda *a, **k: answer())
    with pytest.raises(SystemExit):
        Rest().token()
    assert capsys.readouterr().err == RENDERED


def test_a_500_after_token_renewal_is_reported_once(monkeypatch, capsys):
    """
    Keep the existing one-time 401 renewal and check its final response too.
    """
    responses = iter([answer({'message': 'expired'}, 401), answer()])
    tokens = []

    def request(url, **kwargs):
        tokens.append(kwargs['headers']['x-access-tokens'])
        return next(responses)

    install_session(monkeypatch, request)
    monkeypatch.setattr(Rest, 'token', lambda self: 'renewed-token')
    with pytest.raises(SystemExit):
        Rest().get_raw('node')
    assert tokens == ['cached-token', 'renewed-token']
    assert capsys.readouterr().err == RENDERED


@pytest.mark.parametrize('code', [200, 201, 204, 400, 401, 403, 404, 501, 502, 503, 504])
def test_other_http_codes_keep_their_existing_meaning(code):
    """
    A stream-ending 404 or stopped-service 503 is still returned to its caller.
    """
    response = answer({'message': 'existing response'}, code)
    assert Rest.check_response(response) is response


def test_successful_decoded_and_raw_responses_keep_their_shape(monkeypatch):
    """
    Central error handling must not change successful response contracts.
    """
    body = {'config': {'node': {'node001': {'group': 'compute'}}}}
    raw = answer(body, 200)
    install_session(monkeypatch, lambda *a, **k: raw)
    decoded = Rest().get_data('node')
    assert decoded.status_code == 200
    assert decoded.content == body
    assert Rest().get_raw('config/node') is raw


# ------------------------------------------------------- malformed bodies ----

@pytest.mark.parametrize('raw', [
    b'', b'<html>private proxy page</html>', b'{broken json', b'\xff\xfe',
    b'null', b'[]', b'42', b'"unexpected string"', b'{}',
    b'{"message":null,"detail":null}',
    b'{"message":[],"detail":["not a string"]}',
    b'{"message":"Server Error","detail":"  "}',
])
def test_malformed_500_bodies_use_a_plain_fallback(raw, capsys):
    """
    Missing or non-JSON bodies must not cause another exception or leak HTML.
    """
    response = answer()
    response._content = raw
    with pytest.raises(SystemExit) as exited:
        Rest.check_response(response)
    assert exited.value.code == 1
    assert capsys.readouterr().err == 'HTTP ERROR :: 500 Server Error.\n'


@pytest.mark.parametrize('failure', [RuntimeError, ValueError, RecursionError, MemoryError])
def test_json_decoder_failures_cannot_break_error_reporting(monkeypatch, capsys, failure):
    """
    A secondary decoder failure must leave a useful error and exit code.
    """
    def broken(*args, **kwargs):
        raise failure('secondary decoding failure')

    monkeypatch.setattr('luna.utils.message.json.loads', broken)
    with pytest.raises(SystemExit):
        Rest.check_response(types.SimpleNamespace(status_code=500, content=b'{}'))
    assert capsys.readouterr().err == 'HTTP ERROR :: 500 Server Error.\n'


def test_unreadable_response_content_uses_the_plain_fallback(capsys):
    """
    Reading a response property can fail before JSON decoding starts.
    """
    class BrokenResponse:
        status_code = 500

        @property
        def content(self):
            raise RuntimeError('secondary response failure')

    with pytest.raises(SystemExit):
        Rest.check_response(BrokenResponse())
    assert capsys.readouterr().err == 'HTTP ERROR :: 500 Server Error.\n'


def test_a_logging_failure_does_not_replace_the_daemon_error(monkeypatch, capsys):
    """
    A secondary logging failure still leaves the original reason and exit code.
    """
    def broken(*args, **kwargs):
        raise RuntimeError('secondary logging failure')

    writer = Message()
    monkeypatch.setattr(writer, 'logger', types.SimpleNamespace(debug=broken))
    with pytest.raises(SystemExit) as exited:
        writer.error_exit(answer(), 500)
    assert exited.value.code == 1
    assert capsys.readouterr().err == RENDERED


@pytest.mark.parametrize('unwritable', [False, True])
def test_terminal_encoding_or_write_failures_keep_a_nonzero_exit(monkeypatch, unwritable):
    """
    Use escaped text on older terminals; unavailable stderr must not raise a trace.
    """
    written = []

    class Terminal:
        def write(self, text):
            if unwritable:
                raise OSError('stderr is unavailable')
            text.encode('ascii')
            written.append(text)

    monkeypatch.setattr('luna.utils.message.sys.stderr', Terminal())
    with pytest.raises(SystemExit) as exited:
        Message().error_exit(answer({'message': 'Server Error', 'detail': 'ValueError: caf\u00e9'}), 500)
    assert exited.value.code == 1
    assert written == ([] if unwritable else ['HTTP ERROR :: 500 Server Error\n    ValueError: caf\\xe9\n'])


def test_detail_is_one_line_without_terminal_control_characters():
    """
    Preserve the indentation if an older daemon sends multiline detail.
    """
    assert Message.answer_message({'detail': 'ValueError: first\nsecond\tline\x00'}, 500) == (
        'Server Error\n    ValueError: first second line')


def test_existing_error_writers_share_the_formatter(capsys):
    """
    Raw bodies and decoded bodies use the same indented reason.
    """
    Message().show_error(answer(), 500)
    with pytest.raises(SystemExit):
        Message().show_failed_exit(BODY)
    assert capsys.readouterr().err == RENDERED + f'Server Error\n    {DETAIL}\n'


def test_an_existing_command_message_is_not_replaced_by_the_500_fallback(capsys):
    """
    Preserve a command's already-decoded error string, including older daemon errors.
    """
    with pytest.raises(SystemExit):
        Message().error_exit('database is locked', 500)
    assert capsys.readouterr().err == 'HTTP ERROR :: 500 database is locked.\n'


@pytest.mark.parametrize('code', [403, 404])
def test_other_refusals_keep_the_daemons_message(code, capsys):
    """
    Existing permission and missing-record messages still render as plain text.
    """
    with pytest.raises(SystemExit):
        Message().error_exit(answer({'message': 'operation is not permitted'}, code), code)
    assert capsys.readouterr().err == 'operation is not permitted.\n'


# --------------------------------------------------------- status followers ----

@pytest.mark.parametrize('route', ['config', 'control'])
def test_status_followers_stop_after_one_http_500(monkeypatch, capsys, route):
    """
    The REST check stops a follower before it can keep polling or lose the reason.
    """
    calls = []

    def request(url, **kwargs):
        calls.append(url)
        return answer()

    install_session(monkeypatch, request)
    monkeypatch.setattr('luna.utils.helper.sleep', lambda seconds: None)
    with pytest.raises(SystemExit):
        Helper().dig_status('req-1', 1, 'power', route=route)
    assert calls == [f'https://daemon/{route}/status/req-1']
    assert capsys.readouterr().err == RENDERED


def test_a_job_failure_in_http_200_is_still_followed_to_the_end(monkeypatch, capsys):
    """
    A job's status field differs from an HTTP 500 from the daemon itself.
    """
    replies = iter([answer({'message': 'job failed', 'status': 500}, 200), answer({}, 404)])
    install_session(monkeypatch, lambda *a, **k: next(replies))
    monkeypatch.setattr('luna.utils.helper.sleep', lambda seconds: None)
    assert Helper().dig_status('req-1', 1, 'power', route='config') is False
    printed = capsys.readouterr()
    assert '[FAILED] job failed' in printed.out
    assert printed.err == ''


@pytest.mark.parametrize('job', [
    'clone_osimage', 'pack_osimage', 'updatecerts_osimage', 'kernel_osimage',
    'grab_osimage', 'push_osimage', 'service_action', 'action_status',
])
def test_progress_processes_are_closed_when_the_shared_check_exits(monkeypatch, capsys, job):
    """
    Every older follower releases its spinner when a real REST call answers 500.
    """
    from luna.control import Control
    from luna.osimage import OSImage
    from luna.service import Service
    processes, polls = [], []

    class Process:
        def __init__(self, *args, **kwargs):
            self.terminated = False
            processes.append(self)

        def start(self):
            pass

        def terminate(self):
            self.terminated = True

    def request(url, **kwargs):
        if 'status/' in url or job == 'action_status':
            polls.append(url)
            assert len(polls) == 1, 'an HTTP 500 must end the follower'
            return answer()
        return answer({'message': 'queued', 'request_id': 'req-1'}, 200)

    install_session(monkeypatch, request)
    monkeypatch.setattr(Helper, 'prepare_payload', lambda self, table, data: data)
    monkeypatch.setattr(Helper, 'get_hostlist', lambda self, hosts: ['node001', 'node002'])
    monkeypatch.setattr(Helper, 'luna_hostlist', lambda self, hosts: hosts)
    for module in ['luna.utils.helper', 'luna.osimage', 'luna.service', 'luna.control']:
        monkeypatch.setattr(module + '.Process', Process)
        monkeypatch.setattr(module + '.sleep', lambda seconds: None, raising=False)
    cls = Helper if job in ('grab_osimage', 'push_osimage') else (
        Service if job == 'service_action' else Control if job == 'action_status' else OSImage)
    instance = cls.__new__(cls)
    instance.logger = logging.getLogger('luna2-cli-tests')
    instance.table, instance.route = 'osimage', 'service' if cls is Service else 'control'
    instance.action_timeout = 20
    instance.args = {'name': 'compute', 'newosimage': 'copy', 'service': 'dhcp',
                     'action': 'status' if cls is Control else 'restart', 'node': 'node[001-002]',
                     'system': 'power'}
    with pytest.raises(SystemExit):
        if cls is Helper:
            getattr(instance, job)('node', {'name': 'node001'})
        else:
            getattr(instance, job)()
    assert len(polls) == 1
    assert processes and all(process.terminated for process in processes)
    assert capsys.readouterr().err == RENDERED
