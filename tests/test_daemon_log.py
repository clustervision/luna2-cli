#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2212: read a compact reason from existing controller logs without changing
the daemon. Match only a new, complete Flask exception for the requested path
and method. Old, ambiguous, rotated or unreadable logs leave a safe HTTP error.

Use temporary files and a fake HTTP transport; no running daemon is required.
"""

import logging
import pytest
import requests

from luna.utils.daemonlog import DaemonLog
from luna.utils.log import Log
from luna.utils.rest import Rest


URL = 'http://127.0.0.1:7050/config/cluster'
TRACE = ('[ERROR]:[2026-10-06 14:02:25,215]:[thread]:[app.py:log_exception@1414]'
         ' - Exception on /config/cluster [GET]\n') + '''\
Traceback (most recent call last):
  File "/trinity/local/python/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/trinity/local/python/lib/python3.10/site-packages/daemon/routes/config_cluster.py", line 60, in config_cluster
    return controller_names + []
TypeError: unsupported operand type(s) for +: 'NoneType' and 'list'
'''
DETAIL = ("TypeError: unsupported operand type(s) for +: 'NoneType' and 'list' "
          "(routes/config_cluster.py:60, in config_cluster)")
FALLBACK = 'HTTP ERROR :: 500 Server Error\n    Daemon traceback unavailable; check the controller daemon log.\n'


@pytest.fixture
def logfile(tmp_path, monkeypatch):
    """
    Isolate the log and avoid dependence on this test host's network settings.
    """
    path = tmp_path / 'daemon.log'
    path.write_text('old log\n', encoding='utf-8')
    monkeypatch.setattr(DaemonLog, 'local_url', lambda url: True)
    monkeypatch.setattr(DaemonLog, 'logfile', lambda: str(path))
    monkeypatch.setattr(Log, '_Log__logger', logging.getLogger('luna2-cli-tests'))
    return path


@pytest.fixture(autouse=True)
def logger(monkeypatch):
    """
    Error output does not depend on controller logging being initialized.
    """
    monkeypatch.setattr(Log, '_Log__logger', logging.getLogger('luna2-cli-tests'))


def response(code=500, url=URL):
    """
    The unchanged daemon sends only Server Error, never a traceback detail.
    """
    result = requests.Response()
    result.status_code, result.url = code, url
    result._content = b'{"message": "Server Error"}'
    return result


def append(path, text=TRACE):
    """
    Append exactly as the daemon's file logger does during a request.
    """
    with path.open('a', encoding='utf-8') as stream:
        stream.write(text)


def test_generic_500_is_enriched_from_new_log_bytes(logfile, capsys):
    """
    Keep the normal HTTP prefix and show only the final location and exception.
    """
    append(logfile, TRACE.replace('TypeError:', 'OldError:'))

    def transport(url, **kwargs):
        append(logfile)
        return response()

    with pytest.raises(SystemExit) as exited:
        Rest.request(transport, 'get', URL)
    assert exited.value.code == 1
    rendered = capsys.readouterr().err
    assert rendered == f'HTTP ERROR :: 500 Server Error\n    {DETAIL}\n'
    assert 'Traceback' not in rendered and 'controller_names' not in rendered
    assert '/trinity/' not in rendered and 'OldError' not in rendered


@pytest.mark.parametrize('method', ['get', 'post', 'put', 'patch', 'delete'])
def test_method_and_query_are_matched(logfile, method):
    """
    Query arguments are not logged by Flask; the method and route must agree.
    """
    url = URL + '?name=node001'
    snapshot = DaemonLog.capture(url, method)
    append(logfile, TRACE.replace('[GET]', '[' + method.upper() + ']'))
    assert DaemonLog.detail(snapshot, response(url=url)) == DETAIL


@pytest.mark.parametrize('text', [
    '', TRACE.replace('/config/cluster [GET]', '/config/node [GET]'),
    TRACE.replace('[GET]', '[POST]'), TRACE + TRACE, TRACE.rstrip('\n'),
    TRACE.replace('Traceback (most recent call last):', 'missing traceback'),
    TRACE.replace('TypeError:', 'malformed exception'),
    TRACE + 'private multiline continuation\n',
    TRACE.replace('app.py:log_exception', 'other.py:log_exception'),
    TRACE.replace('TypeError:', '[INFO]:[time]:[thread]:[file] - interleaved\nTypeError:'),
])
def test_missing_incomplete_or_ambiguous_trace_is_not_selected(logfile, text):
    """
    A mismatch is safer than presenting another call's error as this one's.
    """
    snapshot = DaemonLog.capture(URL, 'get')
    append(logfile, text)
    assert DaemonLog.detail(snapshot, response()) is None


def test_old_matching_trace_is_ignored(logfile):
    """
    A deliberate abort(500) with no new traceback must not reuse yesterday's.
    """
    append(logfile)
    snapshot = DaemonLog.capture(URL, 'get')
    assert DaemonLog.detail(snapshot, response()) is None


def test_unrelated_errors_do_not_hide_one_matching_trace(logfile):
    """
    Concurrent failures on different routes are separable in existing logs.
    """
    snapshot = DaemonLog.capture(URL, 'get')
    append(logfile, TRACE.replace('/config/cluster [GET]', '/config/node [GET]') + TRACE)
    assert DaemonLog.detail(snapshot, response()) == DETAIL


@pytest.mark.parametrize('change', ['rotate', 'truncate', 'regrow', 'oversize', 'remove'])
def test_file_changes_fall_back(logfile, change):
    """
    Rotation, truncation, replacement and excessive output cannot reuse stale data.
    """
    snapshot = DaemonLog.capture(URL, 'get')
    if change == 'rotate':
        logfile.rename(logfile.with_suffix('.old'))
        logfile.write_text('', encoding='utf-8')
    elif change == 'remove':
        logfile.unlink()
        assert DaemonLog.detail(snapshot, response()) is None
        return
    elif change in ('truncate', 'regrow'):
        logfile.write_text('' if change == 'truncate' else 'changed log\n', encoding='utf-8')
    elif change == 'oversize':
        append(logfile, 'x' * DaemonLog.LIMIT)
    append(logfile)
    assert DaemonLog.detail(snapshot, response()) is None


@pytest.mark.parametrize('redirect', [False, True])
def test_redirect_or_different_endpoint_cannot_read_local_trace(logfile, redirect):
    """
    A remote or redirected response must not be paired with this controller's log.
    """
    snapshot = DaemonLog.capture(URL, 'get')
    append(logfile)
    result = response(url=URL if redirect else 'http://elsewhere/config/cluster')
    result.history = [response(302)] if redirect else []
    assert DaemonLog.detail(snapshot, result) is None


@pytest.mark.parametrize('stage', ['capture', 'detail'])
@pytest.mark.parametrize('failure', [PermissionError, OSError, ValueError, MemoryError])
def test_reporting_failures_keep_generic_500(logfile, monkeypatch, capsys, stage, failure):
    """
    Even unexpected inspection failures must preserve exit status and the HTTP error.
    """
    def broken(*args, **kwargs):
        raise failure('secondary reporting failure')

    monkeypatch.setattr(DaemonLog, stage, broken)
    with pytest.raises(SystemExit) as exited:
        Rest.request(lambda *args, **kwargs: response(), 'get', URL)
    assert exited.value.code == 1
    assert capsys.readouterr().err == FALLBACK


@pytest.mark.parametrize('code', [200, 400, 401, 403, 404, 503])
def test_other_status_codes_do_not_read_log(logfile, monkeypatch, code):
    """
    Only an actual HTTP 500 asks the reporter to inspect new log bytes.
    """
    def unexpected(*args):
        pytest.fail('Non-500 responses must not read daemon log content')

    monkeypatch.setattr(DaemonLog, 'detail', unexpected)
    result = response(code)
    assert Rest.request(lambda *args, **kwargs: result, 'get', URL) is result


def test_chained_exception_uses_final_frame_and_reason():
    """
    A new exception raised from another one should show the final cause in the chain.
    """
    chain = TRACE + '\nThe above exception was the direct cause of the following exception:\n\n'
    chain += ('Traceback (most recent call last):\n  File "/external/model.py", line 105, in update\n'
              '    raise ValueError()\nValueError: invalid model\n')
    assert DaemonLog.parse(chain, '/config/cluster', 'GET') == 'ValueError: invalid model (model.py:105, in update)'


@pytest.mark.parametrize('exception', ['Exception: failed', 'package.CustomFailure: failed', 'KeyboardInterrupt'])
def test_plain_and_custom_exception_types(exception):
    """
    A Python exception does not have to end in Error or include any message.
    """
    trace = TRACE.rsplit('TypeError:', 1)[0] + exception + '\n'
    assert DaemonLog.parse(trace, '/config/cluster', 'GET') == (
        f'{exception} (routes/config_cluster.py:60, in config_cluster)')


def test_syntax_error_location_without_function():
    """
    Syntax errors can add an innermost file and line without a function name.
    """
    trace = TRACE.rsplit('TypeError:', 1)[0]
    trace += '  File "/daemon/utils/model.py", line 105\n    invalid syntax\nSyntaxError: invalid syntax\n'
    assert DaemonLog.parse(trace, '/config/cluster', 'GET') == 'SyntaxError: invalid syntax (utils/model.py:105)'


def test_multiline_exception_with_identifier_continuation_is_rejected():
    """
    An identifier on a continuation line must not replace the true exception type.
    """
    assert DaemonLog.parse(TRACE + 'continuation\n', '/config/cluster', 'GET') is None


def test_log_content_is_bounded_and_terminal_controls_are_removed():
    """
    Display strings stay compact and cannot inject terminal escape sequences.
    """
    text = TRACE.replace("unsupported operand type(s) for +: 'NoneType' and 'list'", '\x1b[31m' + 'x' * 4000)
    detail = DaemonLog.parse(text, '/config/cluster', 'GET')
    assert '\x1b' not in detail and len(detail) < 1200


def test_remote_endpoint_is_not_inspected(monkeypatch):
    """
    No automatic SSH or local log lookup for a remote controller.
    """
    monkeypatch.setattr(DaemonLog, 'local_url', lambda url: False)
    monkeypatch.setattr(DaemonLog, 'logfile', lambda: pytest.fail('Remote log inspected'))
    assert DaemonLog.capture('https://remote/config/cluster', 'get') is None


def test_local_address_check_and_proxy_exclusion(monkeypatch):
    """
    Bind only to locally owned addresses, and decline endpoints reached through a proxy.
    """
    monkeypatch.setattr('luna.utils.daemonlog.get_environ_proxies', lambda url: {})
    assert DaemonLog.local_url(URL) is True
    assert DaemonLog.capture('http://192.0.2.1/config/cluster', 'get') is None
    monkeypatch.setattr('luna.utils.daemonlog.get_environ_proxies', lambda url: {'http': 'http://proxy'})
    assert DaemonLog.local_url(URL) is False


def test_explicit_session_proxy_skips_log_capture(monkeypatch, capsys):
    """
    Session proxies also prevent pairing a proxied request with a local daemon log.
    """
    class Session:
        proxies = {'http': 'http://proxy'}

        def get(self, *args, **kwargs):
            return response()

    monkeypatch.setattr(DaemonLog, 'capture', lambda *args: pytest.fail('Proxied log inspected'))
    with pytest.raises(SystemExit):
        Rest.request(Session().get, 'get', URL)
    assert capsys.readouterr().err == FALLBACK


def test_daemon_configuration_selects_log_path(tmp_path, monkeypatch):
    """
    A custom daemon log path is read from its own INI, without changing that file.
    """
    path = tmp_path / 'luna.ini'
    path.write_text('[LOGGER]\nLOGFILE = /custom/daemon.log\n', encoding='utf-8')
    monkeypatch.setattr('luna.utils.daemonlog.DAEMON_INI_FILE', str(path))
    assert DaemonLog.logfile() == '/custom/daemon.log'
    path.write_text('malformed ini', encoding='utf-8')
    assert DaemonLog.logfile() == '/var/log/luna/luna2-daemon.log'
