"""
TRIX-2217: an install_mode override on a node or a group is cleared by an empty value, which
the daemon already stores as "inherit again". The CLI must let the empty value through.
"""
import argparse
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _parser(entity):
    from luna.group import Group
    from luna.node import Node
    cls = {'group': Group, 'node': Node}[entity]
    instance = cls.__new__(cls)
    instance.table = entity
    instance.route = entity
    instance.logger = logging.getLogger('luna2-cli-tests')
    parser = argparse.ArgumentParser(prog='luna')
    instance.get_arguments(parser, parser.add_subparsers(dest='table'))
    return parser


@pytest.mark.parametrize('entity', ['group', 'node'])
def test_an_empty_install_mode_reaches_the_payload(entity):
    from luna.utils.helper import Helper
    args = vars(_parser(entity).parse_args([entity, 'change', 'x', '--install-mode', '']))
    assert args['install_mode'] == ''
    payload = Helper().prepare_payload(entity, args)
    assert payload['install_mode'] == '', 'the empty value is what clears the override'


@pytest.mark.parametrize('entity', ['group', 'node'])
def test_a_real_mode_still_parses_and_a_wrong_one_is_refused(entity):
    args = vars(_parser(entity).parse_args([entity, 'change', 'x', '--install-mode', 'memboot']))
    assert args['install_mode'] == 'memboot'
    with pytest.raises(SystemExit):
        _parser(entity).parse_args([entity, 'change', 'x', '--install-mode', 'bogus'])
