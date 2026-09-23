#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2087: profile list and show build their tables by hand, so they do not get
the owners, usergroups and access columns every other governed listing gets from
filter_columns. They carry the same three, from the same ACCESS_FIELDS.
"""

import logging

import pytest

import luna.utils.log as luna_log
from luna.utils.constant import ACCESS_FIELDS


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse():
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.content = payload if payload is not None else {}


PROFILE = {'scope': 'static', 'service': 'chronyd', 'action': 'restart', 'enabled': True, 'files': [],
           'owners': 'alice', 'usergroups': 'physics', 'access': 'rwxrwx---'}


@pytest.fixture
def wire(monkeypatch):
    seen = {'tables': []}
    import luna.profile as profile
    monkeypatch.setattr(profile.Rest, 'get_data',
                        lambda self, uri, *a, **k: FakeResponse(payload={'config': {'profiles': {'ntp': dict(PROFILE)}}}),
                        raising=False)
    monkeypatch.setattr(profile.Presenter, 'show_table',
                        lambda self, title, fields, rows: seen['tables'].append((fields, rows)), raising=False)
    monkeypatch.setattr(profile.Presenter, 'show_table_col',
                        lambda self, title, fields, rows: seen['tables'].append((fields, rows)), raising=False)
    return seen


def command(**args):
    from luna.profile import Profile
    cli = Profile.__new__(Profile)
    cli.route, cli.table = 'profiles', 'profile'
    cli.logger = logging.getLogger('luna2-cli-tests')
    cli.args = dict({'name': 'ntp', 'raw': None}, **args)
    return cli


def test_the_list_shows_who_owns_each_profile(wire):
    command().list_profile()
    fields, rows = wire['tables'][0]
    assert fields[-3:] == ACCESS_FIELDS
    assert rows[0][-3:] == ['alice', 'physics', 'rwxrwx---']


def test_the_show_carries_the_same_three(wire):
    command().show_profile()
    fields, rows = wire['tables'][0]
    shown = dict(zip(fields, rows))
    assert {field: shown[field] for field in ACCESS_FIELDS} == {
        'owners': 'alice', 'usergroups': 'physics', 'access': 'rwxrwx---'}
