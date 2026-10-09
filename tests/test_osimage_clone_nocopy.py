"""
luna osimage clone: a clone that copies nothing is created on the spot and the daemon answers
201 without a request id, like any other add. That is a finished clone, not a failure.
"""
import types

import pytest

from test_login_and_credentials import home  # noqa: F401  a controller ini of our own


def _answer(code, content):
    return types.SimpleNamespace(status_code=code, content=content)


@pytest.fixture
def daemon(home, monkeypatch):
    import luna.osimage as osimage
    import luna.utils.helper as helper
    from luna.utils.rest import Rest as RealRest
    sent = []
    fake = types.SimpleNamespace(clone=_answer(201, {'message': 'OS Image cloned successfully'}))

    class Rest(RealRest):
        def __init__(self):
            pass

        def post_clone(self, table=None, name=None, data=None):
            sent.append(data)
            return fake.clone

    from luna.cli import Cli
    # the parser asks the real daemon for its controllers, so it is built before the fake goes in
    parser = Cli().get_parser()
    monkeypatch.setattr(osimage, 'Rest', Rest)
    monkeypatch.setattr(helper, 'Rest', Rest)
    fake.sent = sent
    fake.clone_osimage = lambda *argv: osimage.OSImage(args=vars(parser.parse_args(
        ['osimage', 'clone', *argv])))
    return fake


def test_a_nocopy_clone_is_reported_as_cloned(daemon, capsys):
    daemon.clone_osimage('compute', 'qa-img', '--nocopy', '--bare', '-p', '/trinity/images/qa-img')
    out = capsys.readouterr()
    assert len(daemon.sent) == 1, 'the clone reached the daemon'
    payload = daemon.sent[0]['config']['osimage']['compute']
    assert payload['nocopy'] is True and payload['newosimage'] == 'qa-img'
    assert 'Cloned' in out.out and 'FAILED' not in out.out + out.err


def test_a_refused_clone_still_fails_with_the_daemons_message(daemon, capsys):
    daemon.clone = _answer(404, {'message': 'OS Image compute not present in the database'})
    with pytest.raises(SystemExit):
        daemon.clone_osimage('compute', 'qa-img', '--nocopy')
    assert 'not present in the database' in capsys.readouterr().err
