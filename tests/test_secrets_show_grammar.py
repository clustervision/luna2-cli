#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.
"""
TRIX-1966: one grammar for `luna secrets show` across node, group and cluster. The secret
is optional everywhere and may be given as the positional or as -s; both reach the same
request. Before, node took only -s and group and cluster only a required positional.
"""
import argparse
import logging

import pytest

from luna.utils import log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _parser():
    from luna.secrets import Secrets
    secrets = Secrets.__new__(Secrets)
    secrets.route = 'secrets'
    secrets.logger = logging.getLogger('luna2-cli-tests')
    parser = argparse.ArgumentParser(prog='luna')
    secrets.get_arguments(parser, parser.add_subparsers(dest='table'))
    return parser


@pytest.mark.parametrize('argv, expected', [
    (['secrets', 'show', 'group', 'compute', 'krb5'], 'krb5'),
    (['secrets', 'show', 'group', 'compute', '-s', 'krb5'], 'krb5'),
    (['secrets', 'show', 'group', 'compute'], None),
    (['secrets', 'show', 'cluster', 'krb5'], 'krb5'),
    (['secrets', 'show', 'cluster', '-s', 'krb5'], 'krb5'),
    (['secrets', 'show', 'cluster'], None),
    (['secrets', 'show', 'node', 'node001', 'krb5'], 'krb5'),
    (['secrets', 'show', 'node', 'node001', '-s', 'krb5'], 'krb5'),
    (['secrets', 'show', 'node', 'node001'], None),
])
def test_every_show_form_accepts_the_secret_either_way_or_not_at_all(argv, expected):
    args = vars(_parser().parse_args(argv))
    assert (args.get('secret') or args.get('secret_positional')) == expected


def test_show_sends_the_secret_whichever_way_it_came(monkeypatch):
    """The two fields are merged where the request is built, because an optional positional
    overwrites the flag's value when the flag comes first on the command line."""
    from luna.secrets import Secrets
    seen = []
    class Answer:
        status_code = 200
        content = {'config': {'secrets': {'cluster': []}}}
    monkeypatch.setattr('luna.secrets.Rest', lambda: type('R', (), {'get_data': lambda self, uri: seen.append(uri) or Answer()})())
    monkeypatch.setattr('luna.secrets.Presenter', lambda: type('P', (), {'show_table': lambda self, *a: True, 'show_json': lambda self, *a: True})())
    secrets = Secrets.__new__(Secrets)
    secrets.route = 'secrets'
    secrets.logger = logging.getLogger('luna2-cli-tests')
    for args in ({'entity': 'cluster', 'secret': None, 'secret_positional': 'krb5', 'raw': None},
                 {'entity': 'cluster', 'secret': 'krb5', 'secret_positional': None, 'raw': None},
                 {'entity': 'cluster', 'secret': None, 'secret_positional': None, 'raw': None}):
        secrets.args = args
        secrets.show_secrets()
    assert seen == ['secrets/cluster/krb5', 'secrets/cluster/krb5', 'secrets/cluster']
