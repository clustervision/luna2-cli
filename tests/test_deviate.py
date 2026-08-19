#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
Test battery for `luna group|node list -d`, which answers "what has been changed
away from the defaults" without reading every record by hand.

Three things decide the answer, and each is pinned separately:

  (1) which entries are listed at all -- the daemon's `_override` flag on the
      list payload, nothing else;
  (2) which fields are named against an entry -- a field is deviating only when
      its `_<field>_source` names this table AND the field is one the CLI calls
      overridable, in constant.overrides();
  (3) what those fields are worth in -R, where base64 script content has to come
      back as text and the daemon's stringified 'True'/'False'/'None' have to come
      back as real JSON types.

(2) is the one that fails quietly. A field missing from overrides() does not
error: the entry still lists, its `deviated` cell is just short by one, and the
operator reads a complete answer. The last test in this file closes that class
rather than naming today's fields -- see its docstring.

luna.utils.log refuses to initialise without root, so the logger is stubbed the
way tests/test_brief_disklayout.py stubs it. Nothing else here needs privilege,
a daemon or a database.
"""
from __future__ import annotations

import json
import logging

import pytest

import luna.utils.log as luna_log
from luna.utils.constant import overrides, sortby


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


@pytest.fixture
def helper():
    from luna.utils.helper import Helper
    return Helper()


# A group as GET /config/group/<name> really returns it: every inheritable field
# carried alongside a _<field>_source saying who supplied the value, booleans and
# nulls stringified, script bodies base64. Shortened, but not reshaped.
GROUP_RECORD = {
    'name': 'compute',
    'setupbmc': 'True',
    'kerneloptions': 'net.ifnames=0 biosdevname=0',
    'prescript': 'ZWNobyBoZWxsbwo=',
    'partscript': 'bW91bnQgLXQgdG1wZnMgdG1wZnMgL3N5c3Jvb3QK',
    'netboot': 'True',
    'bootmenu': 'False',
    'provision_interface': 'BOOTIF',
    'provision_method': 'http',
    'provision_fallback': 'http',
    'unmanaged_bmc_users': 'None',
    'ipxe_kernel': 'default',
    'routes': None,
    '_override': True,
    '_setupbmc_source': 'group',
    '_netboot_source': 'group',
    '_bootmenu_source': 'default',
    '_provision_interface_source': 'default',
    '_provision_method_source': 'group',
    '_provision_fallback_source': 'cluster',
    '_kerneloptions_source': 'osimage',
    '_ipxe_kernel_source': 'default',
    '_unmanaged_bmc_users_source': 'bmcsetup',
    '_prescript_source': 'group',
    '_partscript_source': 'group',
}


class FakeResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


class FakeRest:
    """Stands in for luna.utils.rest.Rest so no daemon is needed."""

    served = {}
    calls = []

    def get_data(self, table=None, name=None, data=None):
        FakeRest.calls.append((table, name))
        return FakeResponse({'config': {table: {name: FakeRest.served[name]}}})


@pytest.fixture
def fake_rest(monkeypatch):
    import luna.utils.helper as helper_module
    FakeRest.served, FakeRest.calls = {}, []
    monkeypatch.setattr(helper_module, 'Rest', FakeRest)
    return FakeRest


# ---------------------------------------------------------------- (1) listing

FILTER_CASES = [
    ('flagged entries are kept', {'a': {'_override': True}}, ['a']),
    ('an unflagged entry is dropped', {'a': {'_override': False}}, []),
    ('a missing flag is not an override', {'a': {'name': 'a'}}, []),
    ('the flag alone decides, not the fields',
     {'a': {'_override': False, 'kerneloptions': 'quiet'}}, []),
    ('order is preserved',
     {'a': {'_override': True}, 'b': {'_override': False}, 'c': {'_override': True}},
     ['a', 'c']),
]


@pytest.mark.parametrize('label,data,expected', FILTER_CASES, ids=[c[0] for c in FILTER_CASES])
def test_filter_deviated(helper, label, data, expected):
    assert list(helper.filter_deviated(data)) == expected


# ------------------------------------------------------------- (2) the fields

def test_deviated_field_names_reads_the_sources(helper):
    """Only a field the group supplies itself AND that overrides() knows about."""
    assert helper.deviated_field_names('group', GROUP_RECORD) == [
        'prescript', 'provision_method',
    ]


def test_a_field_inherited_from_elsewhere_is_not_deviating(helper):
    """provision_fallback comes from the cluster here, kerneloptions from the osimage."""
    names = helper.deviated_field_names('group', GROUP_RECORD)
    assert 'provision_fallback' not in names
    assert 'kerneloptions' not in names
    assert 'bootmenu' not in names  # source 'default'


def test_a_field_outside_overrides_is_not_deviating(helper):
    """setupbmc is set on the group and is deliberately not reported.

    overrides() is the gate, not the source field: the record carries a source
    for far more fields than the CLI calls overridable, and the extra ones are
    not deviations from anything a parent supplied.
    """
    assert GROUP_RECORD['_setupbmc_source'] == 'group'
    assert 'setupbmc' not in helper.deviated_field_names('group', GROUP_RECORD)


def test_the_group_script_fields_are_not_symmetrical(helper):
    """A group's partscript and postscript never report as deviating; its prescript does.

    A node treats all three the same way. A group does not, because only
    prescript is in overrides('group') -- so a group carrying its own partscript
    lists under -d (the daemon flags it) with partscript absent from the cell.

    Pinned as it stands rather than corrected: which of the three a group can
    meaningfully be said to override is a question for whoever owns the field
    lists, and widening it here would change what `group show` stars as well.
    """
    assert GROUP_RECORD['_partscript_source'] == 'group'
    names = helper.deviated_field_names('group', GROUP_RECORD)
    assert 'prescript' in names
    assert 'partscript' not in names
    assert 'postscript' not in names


def test_deviated_fields_is_the_names_comma_separated(helper):
    assert helper.deviated_fields('group', GROUP_RECORD) == 'prescript, provision_method'


def test_a_record_with_nothing_of_its_own_names_no_fields(helper):
    record = {'name': 'plain', 'provision_method': 'http', '_provision_method_source': 'cluster'}
    assert helper.deviated_field_names('group', record) == []
    assert helper.deviated_fields('group', record) == ''


# ------------------------------------------------------------- (3) the values

def test_deviated_values_decodes_and_normalises(helper):
    values = helper.deviated_values('group', GROUP_RECORD)
    assert values == {
        'prescript': 'echo hello\n',      # base64 in the record, text here
        'provision_method': 'http',
    }


VALUE_CASES = [
    ('a stringified true becomes a real boolean', 'setupbmc', 'True', True),
    ('a stringified false becomes a real boolean', 'setupbmc', 'False', False),
    ('a stringified none becomes null', 'setupbmc', 'None', None),
    ('a plain string is left alone', 'provision_method', 'http', 'http'),
]


@pytest.mark.parametrize('label,field,stored,expected', VALUE_CASES,
                         ids=[c[0] for c in VALUE_CASES])
def test_deviated_value_types(helper, label, field, stored, expected):
    record = {field: stored, f'_{field}_source': 'node'}
    assert helper.deviated_values('node', record) == {field: expected}


def test_deviated_values_survive_json(helper):
    """-R prints through json.dumps, so every value has to be serialisable."""
    json.dumps(helper.deviated_values('group', GROUP_RECORD))


# ------------------------------------------------------------- the render path

def test_the_table_view_names_the_fields(helper, fake_rest, capsys):
    fake_rest.served = {'compute': GROUP_RECORD}
    helper.show_deviated('group', {'compute': {'_override': True}}, {'raw': None})
    out = capsys.readouterr().out
    assert 'compute' in out
    assert 'prescript, provision_method' in out


def test_the_raw_view_carries_the_values(helper, fake_rest, capsys):
    fake_rest.served = {'compute': GROUP_RECORD}
    helper.show_deviated('group', {'compute': {'_override': True}}, {'raw': True})
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        'compute': {
            'name': 'compute',
            'deviated': {
                'prescript': 'echo hello\n',
                'provision_method': 'http',
            },
        }
    }


def test_one_record_is_read_per_listed_entry(helper, fake_rest):
    """The list payload does not carry the *_source fields, so each entry is re-read.

    Pinned because it is the cost of the flag: -d is one request per deviating
    entry, not one request. Anything that changes that has changed what the
    command costs on a cluster, and should be a deliberate decision.
    """
    fake_rest.served = {'compute': GROUP_RECORD, 'gpu': GROUP_RECORD}
    helper.show_deviated('group', {'compute': {}, 'gpu': {}}, {'raw': None})
    assert fake_rest.calls == [('group', 'compute'), ('group', 'gpu')]


# ------------------------------------------------------ the class, not the case

@pytest.mark.parametrize('table', ['node', 'group'])
def test_every_overridable_field_is_a_field_the_cli_displays(table):
    """overrides() and sortby() are two hand-written lists over the same fields.

    A name that drifts out of step -- renamed upstream, or typed slightly wrong --
    does not fail: the field simply stops being reported as deviating, and both
    `show`'s '*' marker and `list -d` quietly go one field short of the truth.
    Deriving the check from the lists themselves means the next field added is
    covered without anyone remembering this test exists.
    """
    unknown = sorted(set(overrides(table)) - set(sortby(table)))
    assert not unknown, f'{table}: overrides() names fields sortby() does not: {unknown}'
