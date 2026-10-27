"""
TRIX-2194: luna control on a hostlist the daemon refuses as a whole. The daemon answers at
once with a 403 naming the node outside the caller's scope; the CLI must show that answer
and exit non-zero, instead of printing nothing behind a spinner that never stops.
"""
import json
import logging

import pytest

import luna.utils.log as luna_log

REFUSAL = 'not permitted for 1 of 2 nodes: node001 (node node001 is not available)'


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse():
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.payload = payload
        self.content = json.dumps(payload).encode()

    def json(self):
        return self.payload


@pytest.fixture
def daemon(monkeypatch):
    import luna.control as control
    state = {'answer': FakeResponse(403, {'message': REFUSAL}), 'spinner_stopped': 0, 'printed': 0}
    monkeypatch.setattr(control.Rest, 'post_raw', lambda self, uri, payload: state['answer'], raising=False)
    monkeypatch.setattr(control.Helper, 'get_hostlist', lambda self, node: node.split(','))
    monkeypatch.setattr(control.Helper, 'control_print', lambda self, *a, **k: state.update(printed=state['printed'] + 1) or 0)

    class NoProcess():
        def __init__(self, *a, **k):
            pass

        def start(self):
            pass

        def terminate(self):
            state['spinner_stopped'] += 1
    monkeypatch.setattr(control, 'Process', NoProcess)
    return state


def _status_on(hostlist):
    from luna.control import Control
    instance = Control.__new__(Control)
    instance.logger = luna_log.Log.get_logger()
    instance.args = {'system': 'power', 'action': 'status', 'node': hostlist}
    instance.route = 'control'
    instance.action_timeout = 30
    return instance.action_status()


def test_a_refused_hostlist_shows_the_daemons_answer_and_fails(daemon, capsys):
    with pytest.raises(SystemExit) as stop:
        _status_on('qa-node01,node001')
    assert stop.value.code == 1
    assert REFUSAL in capsys.readouterr().err
    assert daemon['spinner_stopped'] == 1, 'the spinner must not outlive the refusal'


def test_an_accepted_hostlist_still_prints_the_table(daemon):
    daemon['answer'] = FakeResponse(200, {'control': {'power': {'ok': {}}, 'failed': {}}})
    _status_on('qa-node01,node001')
    assert daemon['printed'] == 1 and daemon['spinner_stopped'] == 1
