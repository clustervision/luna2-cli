"""
luna node clone: the list it fetches first only skips names already taken. A person who may
read no node gets 404 for that list, and the clone still reaches the daemon, whose answer is shown.
"""
import types

import pytest

from test_login_and_credentials import home  # noqa: F401  a controller ini of our own


def _answer(code, content):
    return types.SimpleNamespace(status_code=code, content=content)


@pytest.fixture
def daemon(home, monkeypatch):
    import luna.node as node
    import luna.utils.helper as helper
    from luna.utils.rest import Rest as RealRest
    sent = []
    fake = types.SimpleNamespace(list=_answer(404, 'No nodes available'),
                                 clone=_answer(404, 'node qa-node03 is not available'))

    class Rest(RealRest):
        def __init__(self):
            pass

        def get_data(self, table=None, name=None, data=None):
            return fake.list

        def post_clone(self, table=None, name=None, data=None):
            sent.append(data)
            return fake.clone
    from luna.cli import Cli
    # the parser asks the real daemon for its controllers, so it is built before the fake goes in
    parser = Cli().get_parser()
    monkeypatch.setattr(node, 'Rest', Rest)
    monkeypatch.setattr(helper, 'Rest', Rest)
    fake.sent = sent
    fake.clone_node = lambda source, new: node.Node(args=vars(parser.parse_args(['node', 'clone', source, new])))
    return fake


def test_a_clone_by_someone_who_sees_no_node_shows_the_daemons_answer(daemon, capsys):
    with pytest.raises(SystemExit):
        daemon.clone_node('qa-node03', 'qa-node04')
    err = capsys.readouterr().err
    assert len(daemon.sent) == 1, 'the clone reached the daemon'
    assert 'node qa-node03 is not available' in err and 'at this moment' not in err


def test_any_other_failure_of_the_list_stops_with_the_daemons_message(daemon, capsys):
    daemon.list = _answer(500, 'database is locked')
    with pytest.raises(SystemExit):
        daemon.clone_node('qa-node03', 'qa-node04')
    assert not daemon.sent
    assert 'database is locked' in capsys.readouterr().err


def test_a_name_already_taken_is_still_skipped(daemon, capsys):
    daemon.list = _answer(200, {'config': {'node': {'qa-node04': {}}}})
    daemon.clone_node('qa-node03', 'qa-node04')
    assert not daemon.sent
    assert 'Node already present in database: qa-node04' in capsys.readouterr().err


@pytest.mark.parametrize('new', ['node[', 'node[05-04]'])
def test_a_name_the_hostlist_cannot_expand_is_refused_not_ignored(daemon, capsys, new):
    with pytest.raises(SystemExit) as stop:
        daemon.clone_node('qa-node03', new)
    assert stop.value.code != 0 and not daemon.sent
    assert f'{new} is not a node name or a hostlist' in capsys.readouterr().err
