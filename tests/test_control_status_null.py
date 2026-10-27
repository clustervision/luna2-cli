"""
TRIX-2242: luna control nextboot status on a node whose BMC gives nothing. The daemon
answers null under the control key, and the CLI must print a status line, not a traceback.
"""
import json
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse():
    def __init__(self, payload):
        self.status_code = 200
        self.payload = payload
        self.content = json.dumps(payload).encode()

    def json(self):
        return self.payload


def _status_for(monkeypatch, payload):
    import luna.control as control
    from luna.control import Control
    monkeypatch.setattr(control.Rest, 'get_raw', lambda self, uri, timeout=None: FakeResponse(payload),
                        raising=False)
    monkeypatch.setattr(control.Helper, 'get_hostlist', lambda self, node: [node])
    shown = {}
    monkeypatch.setattr(control.Presenter, 'show_table_col',
                        lambda self, title, fields, rows: shown.update(rows=rows) or True)
    instance = Control.__new__(Control)
    instance.logger = luna_log.Log.get_logger()
    instance.args = {'system': 'nextboot', 'action': 'status', 'node': 'node002'}
    instance.route = 'control'
    instance.action_timeout = 30
    instance.action_status()
    return shown['rows']


def test_a_null_status_from_the_daemon_prints_a_line_not_a_traceback(monkeypatch):
    rows = _status_for(monkeypatch, {'control': {'nextboot': None}})
    assert rows == ['node002', 'NO message received']


def test_a_real_status_still_shows_as_before(monkeypatch):
    rows = _status_for(monkeypatch, {'control': {'nextboot': 'target=None, enabled=Disabled'}})
    assert rows == ['node002', 'target=None, enabled=Disabled']
