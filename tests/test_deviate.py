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
operator reads a complete answer. Two tests close that class rather than naming
today's fields -- see their docstrings.

**What these tests cannot tell you.** Everything here runs against records this
file builds, so it pins the CLI's rule and nothing about the daemon. If the
payload ever stops carrying `_override` or `_<field>_source`, every test below
still passes and the command renders an empty or wrong answer. That gap is not
closable from this side, so it is named rather than papered over: the check that
does close it is running `list -d` against a real daemon and confirming the fields
it names are exactly the fields `show` stars.

luna.utils.log refuses to initialise without root -- logging.basicConfig cannot
open LOG_FILE -- so the logger is stubbed rather than initialised. That is the
only privilege the module wants; nothing here needs a daemon or a database.
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


# --------------------------------------------------------------- the contract
#
# The CLI reads exactly two things out of the daemon's payload, and nothing here
# should imply it reads more:
#
#   _override               on a LIST entry -- "this one overrides something"
#   _<field>_source         on a SHOW record -- who supplied that field's value
#
# Records below are BUILT from those two, per case. They are deliberately not a
# captured daemon response: a frozen copy of another service's output goes stale
# without any test failing, so the suite would stay green while the CLI rendered
# the wrong thing. Nothing on this side can detect that -- the only check that can
# is running the CLI against a real daemon and comparing `list -d` with the fields
# `show` stars. Keep these tests about the rule, and keep that comparison manual.


def record(**sources):
    """Build a record carrying only the fields a case needs.

    Each keyword is `field=(source, value)` and expands to the field plus its
    `_<field>_source`, which is the whole of what deviated_field_names reads.
    """
    built = {}
    for field, (source, value) in sources.items():
        built[field] = value
        built[f'_{field}_source'] = source
    return built


# One group as a worked example: something of its own, something from each of the
# three places a group can inherit from, and something set locally that is not an
# overridable field at all.
A_GROUP = record(
    provision_method=('group', 'http'),        # its own -> deviates
    provision_fallback=('cluster', 'http'),    # from the cluster
    kerneloptions=('osimage', 'quiet'),        # from the osimage
    unmanaged_bmc_users=('bmcsetup', 'None'),  # from the bmcsetup
    bootmenu=('default', 'False'),             # nothing set it
    setupbmc=('group', 'True'),                # its own, but not overridable
)


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
    assert helper.deviated_field_names('group', A_GROUP) == ['provision_method']


def test_a_field_inherited_from_elsewhere_is_not_deviating(helper):
    """provision_fallback comes from the cluster here, kerneloptions from the osimage."""
    names = helper.deviated_field_names('group', A_GROUP)
    assert 'provision_fallback' not in names
    assert 'kerneloptions' not in names
    assert 'bootmenu' not in names  # source 'default'


def test_a_field_outside_overrides_is_not_deviating(helper):
    """setupbmc is set on the group and is deliberately not reported.

    overrides() is the gate, not the source field: the record carries a source
    for far more fields than the CLI calls overridable, and the extra ones are
    not deviations from anything a parent supplied.
    """
    assert A_GROUP['_setupbmc_source'] == 'group'
    assert 'setupbmc' not in helper.deviated_field_names('group', A_GROUP)


# The fields the daemon resolves in its base64 loop. A group is the ROOT for
# them; a node inherits them from its group. The asymmetry is the whole point.
GROUP_ROOT_FIELDS = ['prescript', 'partscript', 'postscript']


@pytest.mark.parametrize('field', GROUP_ROOT_FIELDS)
def test_a_group_never_deviates_on_a_root_field(helper, field):
    """A group is the root for these -- there is nothing above it to deviate from.

    The daemon resolves them for a group in a loop of their own with no parent
    lookup at all: the source comes back 'group' when the group holds any content
    and 'default' otherwise, and that loop never raises _override. 'group' on a
    group therefore means "set", not "overridden". Reporting it as a deviation
    would name every group that has ever had a partscript.

    A node is the opposite case, and the same daemon loop shows why: it reads the
    group's copy first, marks the source 'group' or 'node' accordingly, and raises
    _override only for 'node'. Hence the next test.
    """
    record = {field: 'ZWNobyBoZWxsbwo=', f'_{field}_source': 'group'}
    assert helper.deviated_field_names('group', record) == []


@pytest.mark.parametrize('field', GROUP_ROOT_FIELDS)
def test_a_node_does_deviate_on_a_root_field(helper, field):
    """All three, symmetrically -- a node genuinely inherits them from its group."""
    record = {field: 'ZWNobyBoZWxsbwo=', f'_{field}_source': 'node'}
    assert helper.deviated_field_names('node', record) == [field]


@pytest.mark.parametrize('field', GROUP_ROOT_FIELDS)
def test_a_node_inheriting_a_root_field_is_not_deviating(helper, field):
    record = {field: 'ZWNobyBoZWxsbwo=', f'_{field}_source': 'group'}
    assert helper.deviated_field_names('node', record) == []


@pytest.mark.parametrize('field', GROUP_ROOT_FIELDS)
def test_the_group_override_list_does_not_carry_a_root_field(field):
    """Stated against the list itself, not only through a record.

    The record tests above would still pass if the field were re-added and the
    source happened not to say 'group'. This one fails the moment the list grows
    a field a group cannot inherit, which is how it got here in the first place.
    """
    assert field not in overrides('group')
    assert field in overrides('node')



@pytest.mark.parametrize('table', ['node', 'group'])
def test_a_record_with_no_source_keys_reports_nothing(helper, table):
    """If the payload ever stops carrying the source keys, report nothing, not nonsense.

    This does not detect such a change -- nothing on this side can. It fixes what
    happens when it arrives: an empty `deviated` cell, which reads as "nothing to
    report" and is wrong but harmless, rather than a traceback or a cell naming
    every field the record happens to hold.
    """
    bare = {'name': 'x', 'provision_method': 'http', 'kerneloptions': 'quiet'}
    assert helper.deviated_field_names(table, bare) == []
    assert helper.deviated_values(table, bare) == {}


def test_deviated_fields_is_the_names_comma_separated(helper):
    assert helper.deviated_fields('group', A_GROUP) == 'provision_method'


def test_a_record_with_nothing_of_its_own_names_no_fields(helper):
    record = {'name': 'plain', 'provision_method': 'http', '_provision_method_source': 'cluster'}
    assert helper.deviated_field_names('group', record) == []
    assert helper.deviated_fields('group', record) == ''


# ------------------------------------------------------------- (3) the values

def test_deviated_values_decodes_and_normalises(helper):
    values = helper.deviated_values('group', A_GROUP)
    assert values == {'provision_method': 'http'}


VALUE_CASES = [
    ('a stringified true becomes a real boolean', 'setupbmc', 'True', True),
    ('a stringified false becomes a real boolean', 'setupbmc', 'False', False),
    ('a stringified none becomes null', 'setupbmc', 'None', None),
    ('a plain string is left alone', 'provision_method', 'http', 'http'),
    # EDITOR_KEYS arrive base64 and must come back as text, or -R prints a blob.
    ('script content comes back decoded', 'prescript', 'ZWNobyBoZWxsbwo=', 'echo hello\n'),
    # kerneloptions is an EDITOR_KEY the daemon nonetheless sends as plain text;
    # base64_decode passes non-base64 through, so it must survive untouched.
    ('plain text in an editor field survives', 'kerneloptions',
     'net.ifnames=0 biosdevname=0', 'net.ifnames=0 biosdevname=0'),
]


@pytest.mark.parametrize('label,field,stored,expected', VALUE_CASES,
                         ids=[c[0] for c in VALUE_CASES])
def test_deviated_value_types(helper, label, field, stored, expected):
    record = {field: stored, f'_{field}_source': 'node'}
    assert helper.deviated_values('node', record) == {field: expected}


def test_deviated_values_survive_json(helper):
    """-R prints through json.dumps, so every value has to be serialisable."""
    json.dumps(helper.deviated_values('group', A_GROUP))


# ------------------------------------------------------------- the render path

def test_the_table_view_names_the_fields(helper, fake_rest, capsys):
    fake_rest.served = {'compute': A_GROUP}
    helper.show_deviated('group', {'compute': {'_override': True}}, {'raw': None})
    out = capsys.readouterr().out
    assert 'compute' in out
    assert 'provision_method' in out


def test_the_raw_view_carries_the_values(helper, fake_rest, capsys):
    fake_rest.served = {'compute': A_GROUP}
    helper.show_deviated('group', {'compute': {'_override': True}}, {'raw': True})
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        'compute': {
            'name': 'compute',
            'deviated': {'provision_method': 'http'},
        }
    }


def test_one_record_is_read_per_listed_entry(helper, fake_rest):
    """The list payload does not carry the *_source fields, so each entry is re-read.

    Pinned because it is the cost of the flag: -d is one request per deviating
    entry, not one request. Anything that changes that has changed what the
    command costs on a cluster, and should be a deliberate decision.
    """
    fake_rest.served = {'compute': A_GROUP, 'gpu': A_GROUP}
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
