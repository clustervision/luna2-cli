#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
Which nodes `luna boot status` counts, and what it reads their state as.

Two ways this goes wrong quietly. A node that finished reports booted and looks
exactly like one that booted a month ago, so a cohort taken from the states alone
shrinks as nodes succeed and the bars never fill. And the monitor route prefixes a
state with the node's own name, so a node named after a step reads as being in it.

Neither shows up as an error. Both show up as a percentage that is simply wrong.
"""

import json
import logging
from datetime import datetime, timedelta

import pytest

import luna.utils.log as luna_log
from luna.boot import Boot


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


@pytest.fixture(name='boot')
def boot_fixture():
    """The class without its constructor, which builds an argument parser."""
    instance = Boot.__new__(Boot)
    instance.args = {}
    return instance


class FakeResponse():
    def __init__(self, payload):
        self.content = json.dumps(payload).encode('utf-8')


def _states(nodes):
    """The shape /monitor/node returns: the state carries the node's name in front."""
    return {'monitor': {'status': {'node': {
        name: {'state': f'{name} {state}', 'updated': updated}
        for name, (state, updated) in nodes.items()}}}}


def test_the_node_name_is_stripped_off_the_state(boot, monkeypatch):
    """
    A node called download01 reporting install.rendered must read as rendered. The
    route hands back 'download01 install.rendered' and the stage match is on a
    substring, so an unstripped prefix places it four stages further on than it is.
    """
    payload = _states({'download01': ('install.rendered', '2026-09-04 10:00:00')})
    monkeypatch.setattr('luna.boot.Rest', lambda: type('R', (), {
        'get_raw': staticmethod(lambda route: FakeResponse(payload))})())
    states = boot.node_states()
    assert states['download01']['state'] == 'install.rendered'
    assert boot.BOOT_STAGES[boot.node_stage(states['download01']['state'])][0] == 'rendered'


def test_nodes_from_an_earlier_boot_are_not_counted(boot):
    """
    The anchor is the oldest report among the nodes still in flight. A node that
    booted last month reported before that and is not part of this boot.
    """
    states = {
        'old01': {'state': 'install.booted', 'updated': '2026-08-01 09:00:00'},
        'new01': {'state': 'install.unpack', 'updated': '2026-09-04 10:00:00'},
        'new02': {'state': 'install.booted', 'updated': '2026-09-04 10:05:00'},
    }
    cohort, anchored = boot.boot_cohort(states, sorted(states))
    assert anchored is True
    assert cohort == ['new01', 'new02']


def test_a_finished_cluster_falls_back_to_every_node(boot):
    """Nothing in flight is not a boot: the answer is the cluster, and it says so."""
    states = {f'node{n}': {'state': 'install.booted', 'updated': '2026-09-04 10:00:00'}
              for n in range(3)}
    cohort, anchored = boot.boot_cohort(states, sorted(states))
    assert anchored is False
    assert len(cohort) == 3


def test_a_straggler_widens_the_cohort_and_is_named(boot):
    """
    A node stuck for days is still in flight, so it holds the anchor back and lets
    more nodes in. That is a dilution, not a distortion - the extra nodes finished,
    so they sit at the top of every bar - and the node responsible is named rather
    than left for someone to work out.
    """
    now = datetime.utcnow()
    # relative, because stuck is measured against the clock: a fixed date here would
    # quietly turn every node in the fixture into a stuck one as it aged
    states = {
        'stuck01': {'state': 'install.unpack',
                    'updated': (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')},
        'done01': {'state': 'install.booted',
                   'updated': (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')},
        'new01': {'state': 'install.rendered',
                  'updated': now.strftime('%Y-%m-%d %H:%M:%S')},
    }
    cohort, anchored = boot.boot_cohort(states, sorted(states))
    assert anchored is True
    assert cohort == ['done01', 'new01', 'stuck01']
    stuck = boot.stuck_nodes(states, cohort)
    assert [node['node'] for node in stuck] == ['stuck01']
    assert stuck[0]['stage'] == 'unpack'


def test_a_booted_node_is_never_stuck(boot):
    """It reported long ago because it finished, not because it stopped."""
    states = {
        'done01': {'state': 'install.booted', 'updated': '2026-08-01 08:00:00'},
        'new01': {'state': 'install.download', 'updated': '2026-09-04 10:00:00'},
    }
    assert [n['node'] for n in boot.stuck_nodes(states, sorted(states))] == ['new01']


def test_a_node_reporting_recently_is_not_stuck(boot):
    """
    The threshold has to actually apply, or every node mid-install is reported as a
    problem the moment the view is opened.
    """
    fresh = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    old = (datetime.utcnow() - timedelta(minutes=Boot.STUCK_MINUTES + 5)).strftime(
        '%Y-%m-%d %H:%M:%S')
    states = {
        'busy01': {'state': 'install.unpack', 'updated': fresh},
        'gone01': {'state': 'install.unpack', 'updated': old},
    }
    assert [n['node'] for n in boot.stuck_nodes(states, sorted(states))] == ['gone01']


def test_the_worst_node_is_the_one_reported_first(boot):
    """The row names one node, so it has to be the one furthest gone."""
    now = datetime.utcnow()
    states = {
        f'node0{n}': {'state': 'install.unpack',
                      'updated': (now - timedelta(hours=n)).strftime('%Y-%m-%d %H:%M:%S')}
        for n in (2, 5, 9)
    }
    assert boot.stuck_nodes(states, sorted(states))[0]['node'] == 'node09'


def test_five_hundred_stuck_nodes_do_not_flood_the_view(boot, monkeypatch, capsys):
    """
    A boot does not fail for one node. It fails for a rack, a switch or an image at a
    time, and the view has to stay the same size when it does - a row per node, or five
    hundred names in one cell, is a view nobody can read at the moment they most need
    to. The stage they stopped in is what identifies the fault at that scale.
    """
    now = datetime.utcnow()
    old = (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    nodes = {f'node{n:04d}': ('install.unpack' if n % 25 else 'install.download', old)
             for n in range(500)}
    payload = _states(nodes)
    monkeypatch.setattr('luna.boot.Rest', lambda: type('R', (), {
        'get_raw': staticmethod(lambda route: FakeResponse(payload))})())
    boot.args = {'group': None, 'all': None, 'raw': None, 'verbose': None}
    boot.show_progress(sorted(nodes))
    printed = capsys.readouterr().out
    assert '500 silent for over' in printed
    assert '480 in unpack' in printed and '20 in download' in printed
    # the whole block, borders and all, stays inside a terminal
    assert max(len(line) for line in printed.splitlines()) < 120, 'the view got wide'
    assert len(printed.splitlines()) < 20, 'the view got long'


def test_verbose_names_a_readable_number_of_them(boot, monkeypatch, capsys):
    """Detail is capped: the rest is a count, not another four hundred names."""
    now = datetime.utcnow()
    old = (now - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    nodes = {f'node{n:04d}': ('install.unpack', old) for n in range(500)}
    payload = _states(nodes)
    monkeypatch.setattr('luna.boot.Rest', lambda: type('R', (), {
        'get_raw': staticmethod(lambda route: FakeResponse(payload))})())
    boot.args = {'group': None, 'all': None, 'raw': None, 'verbose': True}
    boot.show_progress(sorted(nodes))
    printed = capsys.readouterr().out
    assert f'and {500 - Boot.STUCK_LISTED} more' in printed
    assert printed.count('node0') <= Boot.STUCK_LISTED + 2


def test_real_node_names_do_not_widen_the_view(boot, monkeypatch, capsys):
    """
    Capping the count of names bounds the row only if names are short. On a real
    cluster they carry a rack and a position, so the cap is a width and the list
    wraps onto as many rows as it needs.
    """
    old = (datetime.utcnow() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    nodes = {f'compute-rack{n // 40:02d}-node{n % 40:02d}': ('install.unpack', old)
             for n in range(500)}
    payload = _states(nodes)
    monkeypatch.setattr('luna.boot.Rest', lambda: type('R', (), {
        'get_raw': staticmethod(lambda route: FakeResponse(payload))})())
    boot.args = {'group': None, 'all': None, 'raw': None, 'verbose': True}
    boot.show_progress(sorted(nodes))
    printed = capsys.readouterr().out
    assert max(len(line) for line in printed.splitlines()) < 120, 'the view got wide'
    # the wrap can put 'and' on the line above, which is the point of wrapping
    assert '488 more' in printed
