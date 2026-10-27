"""
A refusal reads as its message, not as the answer it travelled in.

The commands that start a job read the raw answer of the daemon, because they need the
job's id from it. When the daemon refused, they printed that answer whole: the bytes of
the JSON around the message. `luna osimage pack`, `luna osimage updatecerts` and
`luna service` did; they now print the message.
"""
import json
import logging
import types

import pytest

import luna.utils.log as luna_log

REFUSAL = 'changing osimage compute is not permitted: you may read and operate it (operator role)'


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class RawAnswer:
    """
    What Rest().get_raw hands back: the answer as it came.
    """

    def __init__(self, status_code, content=b''):
        self.status_code = status_code
        self.content = content

    def json(self):
        return json.loads(self.content)


class Messages:
    said = []

    def show_success(self, message=None):
        Messages.said.append(('success', message))
        return True

    def show_failed_exit(self, message=None):
        Messages.said.append(('failed', message))
        raise SystemExit(1)

    def error_exit(self, message=None, code=None):
        Messages.said.append(('exit', message))
        raise SystemExit(1)


def _refused(code=403, message=REFUSAL):
    return RawAnswer(code, json.dumps({'message': message}).encode())


@pytest.mark.parametrize('answer, expected', [
    (_refused(), REFUSAL),
    (_refused(404, 'osimage compute is not available'), 'osimage compute is not available'),
    (RawAnswer(502, b'<html>Bad Gateway</html>'), '<html>Bad Gateway</html>'),
    (RawAnswer(500, b'{"request_id": "1"}'), '{"request_id": "1"}'),
    (RawAnswer(500, b''), ''),
    (types.SimpleNamespace(status_code=403, content=REFUSAL), REFUSAL),
])
def test_the_message_of_an_answer(answer, expected):
    from luna.utils.helper import Helper
    assert Helper().answer_message(answer) == expected


def _osimage(monkeypatch, answer):
    from luna.osimage import OSImage
    monkeypatch.setattr('luna.osimage.Rest', lambda: type('R', (), {'get_raw': lambda self, *a, **k: answer})())
    monkeypatch.setattr('luna.osimage.Message', Messages)
    Messages.said = []
    osimage = OSImage.__new__(OSImage)
    osimage.table = 'osimage'
    osimage.logger = logging.getLogger('luna2-cli-tests')
    osimage.args = {'name': 'compute'}
    return osimage


@pytest.mark.parametrize('verb, words', [('pack_osimage', 'not Packed'), ('updatecerts_osimage', 'certificates not updated'),
                                         ('cancel_osimage', 'pack not cancelled')])
def test_a_refused_osimage_job_says_why_in_words(monkeypatch, verb, words):
    osimage = _osimage(monkeypatch, _refused())
    with pytest.raises(SystemExit):
        getattr(osimage, verb)()
    assert Messages.said == [('failed', f'[ FAILED ] Image compute {words}: {REFUSAL}.')]


def test_a_refused_service_action_says_why_in_words(monkeypatch):
    from luna.service import Service
    refusal = 'service is not permitted: that is for rootus and admin users'
    monkeypatch.setattr('luna.service.Rest', lambda: type('R', (), {'get_raw': lambda self, *a, **k: _refused(403, refusal)})())
    monkeypatch.setattr('luna.service.Message', Messages)
    Messages.said = []
    service = Service.__new__(Service)
    service.route = 'service'
    service.logger = logging.getLogger('luna2-cli-tests')
    service.args = {'service': 'dhcp', 'action': 'restart'}
    with pytest.raises(SystemExit):
        service.service_action()
    assert Messages.said == [('exit', refusal)]


@pytest.mark.parametrize('verb, table, words', [('grab_osimage', 'node', 'OSImage not grabbed for node node001'),
                                                ('push_osimage', 'node', 'OSImage not pushed for node node001'),
                                                ('push_osimage', 'group', 'OSImage not pushed for group node001')])
@pytest.mark.parametrize('answer, expected', [(_refused(), REFUSAL), (RawAnswer(502, b'<html>Bad Gateway</html>'), '<html>Bad Gateway</html>')])
def test_a_refused_grab_or_push_says_why_in_words(monkeypatch, verb, table, words, answer, expected):
    from luna.utils.helper import Helper
    monkeypatch.setattr('luna.utils.helper.Rest', lambda: type('R', (), {'post_raw': lambda self, *a, **k: answer})())
    monkeypatch.setattr('luna.utils.helper.Message', Messages)
    monkeypatch.setattr(Helper, 'prepare_payload', lambda self, table, data: data)
    Messages.said = []
    with pytest.raises(SystemExit):
        getattr(Helper(), verb)(table, {'name': 'node001', 'osimage': 'compute'})
    assert Messages.said == [('failed', f'[ FAILED ] {words}: {expected}.')]
