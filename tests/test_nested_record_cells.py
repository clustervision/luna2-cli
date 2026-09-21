#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
A cell holding a list of records reads as records, not as a run of lines.

'luna redfishsetup list' showed every account field flush left, one after the
other, so two accounts looked like ten unrelated settings, and the accounts of
one setup ran straight into the next row. 'luna redfishsetup show' indented the
name line along with the rest, so nothing marked where an account started.

Both views now render a record as its identifying line flush left with its
fields indented beneath, and the list view leaves a blank line between rows.
Both go through Helper().nested_lines, and both are pinned here because the two
call sites are the two places the old loop lived.

The list is the overview, so it keeps only an account's name and username, the
way bmcsetup list leaves its credentials to bmcsetup show. Show has all of it.
"""

import logging

import pytest

import luna.utils.log as luna_log
from luna.utils.helper import Helper


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


ACCOUNTS = [
    {'name': 'fwadmin', 'username': 'luna-fwadmin', 'password': 's3cret', 'role': 'Administrator'},
    {'name': 'op', 'username': 'luna-op', 'password': 'hunter2', 'role': 'Operator'},
]

LIST_ACCOUNTS = (
    'name = fwadmin\n'
    '  username = luna-fwadmin\n'
    'name = op\n'
    '  username = luna-op'
)

SHOW_ACCOUNTS = (
    'name = fwadmin\n'
    '  username = luna-fwadmin\n'
    '  password = s3cret\n'
    '  role = Administrator\n'
    'name = op\n'
    '  username = luna-op\n'
    '  password = hunter2\n'
    '  role = Operator'
)


def setup(name):
    return {'name': name, 'scheme': 'https', 'port': None, 'verify': False,
            'accounts': [dict(a) for a in ACCOUNTS]}


def test_list_view_keeps_name_and_username_and_nothing_else():
    fields, rows = Helper().filter_data('redfishsetup', {'hw': setup('hw')})
    accounts = rows[0][fields.index('accounts')]
    assert accounts == LIST_ACCOUNTS
    assert 'password' not in accounts


def test_list_view_leaves_a_blank_line_between_rows_but_not_after_the_last():
    data = {'hw': setup('hw'), 'abc': setup('abc')}
    fields, rows = Helper().filter_data('redfishsetup', data)
    column = fields.index('accounts')
    assert rows[0][column] == LIST_ACCOUNTS + '\n'
    assert rows[1][column] == LIST_ACCOUNTS


def test_show_view_has_the_whole_account_with_its_name_flush_left():
    fields, rows = Helper().filter_data_col('redfishsetup', setup('hw'))
    assert rows[fields.index('accounts')] == SHOW_ACCOUNTS


def test_show_view_still_opens_an_interface_record_on_its_interface_line():
    """Group and node show relied on 'interface' being the heading before; still true."""
    lines = Helper().nested_lines([{'interface': 'BOOTIF', 'network': 'cluster'}])
    assert lines == 'interface = BOOTIF\n  network = cluster'
