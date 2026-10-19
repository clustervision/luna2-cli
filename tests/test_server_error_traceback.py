#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2212: the daemon sends the full traceback of an uncaught exception in its 500
body, unfiltered; the CLI reduces it to its own one-line summary, wherever it runs.
Only a body without a usable traceback, as an older daemon sends, falls back to
the local daemon log as before.

Traceback text comes from the interpreter itself or in the daemon's shape; a fake
HTTP transport and a temporary log file replace the daemon.
"""

import json
import logging
import traceback

import pytest
import requests

from luna.utils.daemonlog import DaemonLog
from luna.utils.log import Log
from luna.utils.rest import Rest


URL = 'http://127.0.0.1:7050/config/cluster'
SENT = '''\
Traceback (most recent call last):
  File "/trinity/local/python/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/trinity/local/luna/daemon/routes/config_cluster.py", line 58, in config_cluster
    raise RuntimeError('qa2212 test')
RuntimeError: qa2212 test
'''
SUMMARY = 'RuntimeError: qa2212 test (routes/config_cluster.py:58, in config_cluster)'
LOGGED = ('[ERROR]:[2026-10-06 14:02:25,215]:[thread]:[app.py:log_exception@1414]'
          ' - Exception on /config/cluster [GET]\n') + SENT.replace('RuntimeError: qa2212 test', 'KeyError: logged')
LOG_SUMMARY = 'KeyError: logged (routes/config_cluster.py:58, in config_cluster)'
FALLBACK = 'HTTP ERROR :: 500 Server Error\n    Daemon traceback unavailable; check the controller daemon log.\n'


@pytest.fixture(autouse=True)
def logger(monkeypatch):
    """
    Error output does not depend on controller logging being initialized.
    """
    monkeypatch.setattr(Log, '_Log__logger', logging.getLogger('luna2-cli-tests'))


@pytest.fixture
def logfile(tmp_path, monkeypatch):
    """
    A local controller log, isolated from this host's files and network settings.
    """
    path = tmp_path / 'daemon.log'
    path.write_text('old log\n', encoding='utf-8')
    monkeypatch.setattr(DaemonLog, 'local_url', lambda url: True)
    monkeypatch.setattr(DaemonLog, 'logfile', lambda: str(path))
    return path


def response(body):
    """
    A daemon 500 with the given JSON body, or raw bytes for a body that is not JSON.
    """
    result = requests.Response()
    result.status_code, result.url = 500, URL
    result._content = body if isinstance(body, bytes) else json.dumps(body).encode()
    return result


def rendered(reason):
    return f'HTTP ERROR :: 500 Server Error\n    {reason}\n'


def failing(capsys, transport):
    """
    Run the real REST boundary and return what the operator sees on stderr.
    """
    with pytest.raises(SystemExit) as exited:
        Rest.request(transport, 'get', URL)
    assert exited.value.code == 1
    return capsys.readouterr().err


def chained_traceback():
    """
    What the daemon sends for an exception raised while another was being handled.
    """
    try:
        try:
            return {}['missing']
        except KeyError:
            raise ValueError('qa2212 chained')
    except ValueError as exception:
        return ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))


def test_the_traceback_the_daemon_sends_is_summarised_and_the_log_is_left_alone(logfile, monkeypatch, capsys):
    """
    With a reason in the body, a different reason in the local log is never read.
    """
    reads = []
    original = DaemonLog.detail

    def detail(snapshot, result):
        reads.append(snapshot)
        return original(snapshot, result)

    def transport(url, **kwargs):
        with logfile.open('a', encoding='utf-8') as stream:
            stream.write(LOGGED)
        return response({'message': 'Server Error', 'detail': SENT})

    monkeypatch.setattr(DaemonLog, 'detail', staticmethod(detail))
    shown = failing(capsys, transport)
    assert shown == rendered(SUMMARY)
    assert reads == []
    assert 'Traceback' not in shown and '/trinity/' not in shown and 'logged' not in shown


def test_a_remote_cli_gets_the_final_exception_of_a_real_chain(monkeypatch, capsys):
    """
    No local log is reachable from another machine; the body alone carries the reason,
    and of a chained traceback only the exception that was answered is shown.
    """
    monkeypatch.setattr(DaemonLog, 'local_url', lambda url: False)
    monkeypatch.setattr(DaemonLog, 'logfile', lambda: pytest.fail('Remote log inspected'))
    sent = chained_traceback()
    assert 'During handling of the above exception' in sent
    shown = failing(capsys, lambda url, **kwargs: response({'message': 'Server Error', 'detail': sent}))
    assert shown.startswith('HTTP ERROR :: 500 Server Error\n    ValueError: qa2212 chained (test_server_error_traceback.py:')
    assert shown.endswith(', in chained_traceback)\n')
    assert 'KeyError' not in shown and 'Traceback' not in shown


@pytest.mark.parametrize('body', [{'message': 'Server Error'}, b'<html>proxy page</html>', b''])
def test_a_500_without_a_detail_still_reads_the_local_log(logfile, capsys, body):
    """
    An older daemon, or a body that is not JSON, keeps the log route as before.
    """
    def transport(url, **kwargs):
        with logfile.open('a', encoding='utf-8') as stream:
            stream.write(LOGGED)
        return response(body)

    assert failing(capsys, transport) == rendered(LOG_SUMMARY)


@pytest.mark.parametrize('logged', [True, False])
@pytest.mark.parametrize('detail', [
    'Server Error', 'RuntimeError: qa2212 test', ['not', 'a', 'string'],
    SENT + 'second line of the message\n',
    SENT.replace('routes/config_cluster.py', 'routes/../config_cluster.py'),
])
def test_a_detail_that_is_not_a_usable_traceback_falls_back_as_before(logfile, capsys, detail, logged):
    """
    Text without frames, a multiline ending or a parent path is never shown as the reason.
    """
    def transport(url, **kwargs):
        if logged:
            with logfile.open('a', encoding='utf-8') as stream:
                stream.write(LOGGED)
        return response({'message': 'Server Error', 'detail': detail})

    shown = failing(capsys, transport)
    assert shown == (rendered(LOG_SUMMARY) if logged else FALLBACK)
    assert 'qa2212' not in shown and 'second line' not in shown
