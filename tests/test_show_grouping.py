#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
`luna node show` and `luna group show` are grouped, and the two agree.

The fields are ordered into blocks - identity, location, BMC, boot, layered
config, install, scripts, provisioning - and divider() draws a rule after the
last field of each. Two things break that quietly, so both are pinned here.

First, a divider is matched against the field name as RENDERED, and a field that
deviates from its parent renders as '<name> *'. Listing only the bare name loses
the rule exactly when a node overrides that field - which is the case an operator
is most likely to be looking at.

Second, node and group share most of their fields, and a reader goes from one to
the other. If the shared fields drift into different orders the two commands stop
feeling like one tool.
"""

import pytest

from luna.utils.constant import divider, sortby


def test_every_divider_is_a_field_that_exists_in_the_order():
    """A rule after a field that is not in the list never draws."""
    for table in ('node', 'group'):
        fields = set(sortby(table))
        missing = [d for d in divider(table)
                   if d.removesuffix(' *') not in fields]
        assert not missing, f'{table}: divider names a field not in sortby: {missing}'


def test_every_divider_has_its_overridden_spelling():
    """
    The trap: helper.py appends ' *' to a field that deviates from its parent,
    and the rule is matched on the rendered name. Bare-name-only means the layout
    silently changes shape on exactly the nodes that differ from their group.
    """
    for table in ('node', 'group'):
        rules = divider(table)
        bare = [d for d in rules if not d.endswith(' *')]
        missing = [f'{d} *' for d in bare if f'{d} *' not in rules]
        assert not missing, f'{table}: divider has no overridden spelling for: {missing}'


def test_node_and_group_agree_on_the_order_of_what_they_share():
    """
    Reading one after the other should not feel like two different tools. Only
    the fields both actually have are compared, so a field unique to either is
    free to sit wherever it belongs.
    """
    node, group = sortby('node'), sortby('group')
    # the two use different names for the same concept
    alias = {'bmcsetupname': 'bmcsetup', 'redfishsetupname': 'redfishsetup'}
    shared = [alias.get(f, f) for f in group if alias.get(f, f) in node]
    in_node_order = [f for f in node if f in shared]
    assert shared == in_node_order, (
        'node and group disagree on the order of their shared fields:\n'
        f'  group order: {shared}\n'
        f'  node order : {in_node_order}')


@pytest.mark.parametrize('table', ['node', 'group'])
def test_the_order_has_no_duplicates(table):
    fields = sortby(table)
    dupes = sorted({f for f in fields if fields.count(f) > 1})
    assert not dupes, f'{table}: field listed twice, so it renders twice: {dupes}'
