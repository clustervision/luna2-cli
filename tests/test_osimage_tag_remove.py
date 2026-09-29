"""
`luna osimage tag remove` must not describe a failure as a success.

A failed removal that came back without a body - the daemon has no route for a tag name
with a '/' in it, for one - was reported as "Tag ... is deleted" while the command exited
with the error code. The message now says the tag could not be removed.
"""
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse:
    def __init__(self, status_code, content=b''):
        self.status_code = status_code
        self.content = content


class Messages:
    said = []

    def show_success(self, message=None):
        Messages.said.append(('success', message))
        return True

    def error_exit(self, message=None, code=None):
        Messages.said.append(('exit', message))
        raise SystemExit(code)


def _remove(monkeypatch, response):
    from luna.osimage import OSImage
    monkeypatch.setattr('luna.osimage.Rest', lambda: type('R', (), {'get_raw': lambda self, route: response})())
    monkeypatch.setattr('luna.osimage.Message', Messages)
    Messages.said = []
    osimage = OSImage.__new__(OSImage)
    osimage.table = 'osimage'
    osimage.logger = logging.getLogger('luna2-cli-tests')
    osimage.args = {'name': 'ubuntu', 'tag': 'a/b'}
    return osimage


def test_a_failure_without_a_body_is_not_called_a_success(monkeypatch):
    osimage = _remove(monkeypatch, FakeResponse(404))
    with pytest.raises(SystemExit) as exited:
        osimage.remove_tag()
    assert exited.value.code == 404
    assert Messages.said == [('exit', 'Tag a/b could not be removed from ubuntu.')]


def test_a_removal_still_reports_success(monkeypatch):
    osimage = _remove(monkeypatch, FakeResponse(204))
    osimage.remove_tag()
    assert Messages.said == [('success', 'OSImage ubuntu Tag a/b is removed.')]
