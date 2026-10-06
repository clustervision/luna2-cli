#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
The node list behind `luna boot status --list`.

It answers what the bars cannot: which nodes are holding the boot back. So it has to
leave out exactly the nodes that booted, keep everything else, read failed from the
daemon's own classification and stuck from the same rule as the summary line.
"""

import json
import logging
from datetime import datetime, timedelta

import pytest

import luna.utils.log as luna_log
from luna.boot import Boot


@pytest.fixture(autouse=True)
def _stub_logger():
    """
    A logger without Log.init_log()'s root-only file handler.
    """
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _ago(minutes):
    return (datetime.utcnow() - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')


def _boot(states, args=None):
    """
    The class without its constructor, reading these states instead of the daemon.
    """
    instance = Boot.__new__(Boot)
    instance.args = args or {}
    instance.node_states = lambda: states
    return instance


NODES = {'node001': {'group': 'compute'}, 'node002': {'group': 'compute'},
         'node003': {'group': 'gpu'}, 'node004': {'group': 'gpu'}}


def test_only_nodes_that_have_not_booted_are_listed_by_name():
    states = {
        'node004': {'state': 'install.download', 'status': '200', 'updated': _ago(3)},
        'node002': {'state': 'install.booted', 'status': '200', 'updated': _ago(2)},
        'node001': {'state': 'install.success', 'status': '200', 'updated': _ago(1)},
        'node003': {'state': 'install.lpart.part', 'status': '200', 'updated': _ago(4)},
    }
    rows = _boot(states).not_booted(NODES, sorted(NODES))
    assert [row['node'] for row in rows] == ['node001', 'node003', 'node004']
    assert [row['stage'] for row in rows] == ['success', 'unpack', 'download']
    assert rows[1]['group'] == 'gpu' and rows[1]['step'] == 'lpart.part'
    assert all(row['condition'] == '' for row in rows)


def test_a_state_the_daemon_classes_as_failed_is_marked_failed():
    states = {
        'node001': {'state': 'install.error', 'status': '500', 'updated': _ago(2)},
        'node002': {'state': 'install.unpack', 'status': '200', 'updated': _ago(2)},
    }
    rows = _boot(states).not_booted(NODES, sorted(NODES))
    assert {row['node']: row['condition'] for row in rows} == {'node001': 'failed',
                                                               'node002': ''}


def test_stuck_uses_the_same_threshold_as_the_summary_line():
    limit = Boot.STUCK_MINUTES
    states = {
        'node001': {'state': 'install.prescript', 'status': '200', 'updated': _ago(limit + 5)},
        'node002': {'state': 'install.prescript', 'status': '200', 'updated': _ago(limit - 5)},
        'node003': {'state': 'install.unpack', 'status': '200', 'updated': _ago(1)},
    }
    boot = _boot(states)
    rows = {row['node']: row for row in boot.not_booted(NODES, sorted(NODES))}
    assert rows['node001']['condition'] == 'stuck'
    assert rows['node002']['condition'] == ''
    assert rows['node001']['minutes'] >= limit
    assert [node['node'] for node in boot.stuck_nodes(states, sorted(states))] == ['node001']


def test_a_node_that_has_not_booted_is_listed_however_long_ago_it_reported():
    """
    A node not yet booted is in flight, and the oldest in-flight report is what anchors
    the boot, so a node silent since last month pulls the boot back to include itself.
    The list therefore never needs --all to show a node that is holding things up.
    """
    states = {
        'node001': {'state': 'install.prescript', 'status': '200', 'updated': '2026-08-01 09:00:00'},
        'node002': {'state': 'install.booted', 'status': '200', 'updated': '2026-07-01 08:00:00'},
        'node003': {'state': 'install.unpack', 'status': '200', 'updated': _ago(1)},
    }
    rows = _boot(states).not_booted(NODES, sorted(NODES))
    assert [row['node'] for row in rows] == ['node001', 'node003']
    assert rows[0]['condition'] == 'stuck'


def test_all_adds_the_nodes_that_carry_no_timestamp():
    """
    Only a node with no stamp falls outside an anchored boot - an older daemon's row.
    """
    states = {
        'node001': {'state': 'install.prescript', 'status': '200', 'updated': None},
        'node003': {'state': 'install.unpack', 'status': '200', 'updated': _ago(1)},
    }
    in_boot = _boot(states).not_booted(NODES, sorted(NODES))
    every = _boot(states, {'all': True}).not_booted(NODES, sorted(NODES))
    assert [row['node'] for row in in_boot] == ['node003']
    assert [row['node'] for row in every] == ['node001', 'node003']
    assert every[0]['minutes'] is None


def test_the_status_the_daemon_classified_the_state_with_is_kept(monkeypatch):
    """
    Failed comes from this field; dropped on the way in, no node is ever failed.
    """
    payload = {'monitor': {'status': {'node': {
        'node001': {'state': 'node001 install.error', 'status': '500',
                    'updated': '2026-09-04 10:00:00'}}}}}
    response = type('Response', (), {'content': json.dumps(payload).encode('utf-8')})()
    monkeypatch.setattr('luna.boot.Rest', lambda: type('R', (), {
        'get_raw': staticmethod(lambda route: response)})())
    instance = Boot.__new__(Boot)
    instance.args = {}
    assert instance.node_states()['node001']['status'] == '500'
