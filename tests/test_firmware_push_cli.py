#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-1996a: what `luna node firmwarepush` sends, and what a dry run shows back.

Two things are worth pinning. A dry run must record nothing - it is the command an
operator runs on four thousand nodes before deciding, so if it posted anything it
would be the opposite of what it says on the tin. And the skips must be reported as
counts by cause rather than a line per node: at cluster scale they share a handful of
reasons, and a wall of them buries the nodes that would actually change.
"""

import json
import logging

import pytest

import luna.utils.log as luna_log


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

    def json(self):
        return self.content


PREVIEW = {'config': {'firmware': {'preview': {
    'ready': [
        {'node': 'node001', 'hardware': ['Dell Inc.', 'PowerEdge R650'],
         'components': [], 'differs': [
             {'component': 'BMC', 'entry': 'dellbmc', 'wanted': '7.10',
              'running': '7.00', 'updateable': True, 'imagefile': 'bmc-7.10.bin'},
             {'component': 'BIOS', 'entry': 'dellbios', 'wanted': '1.05',
              'running': None, 'updateable': True, 'imagefile': 'bios-1.05.bin'}]},
        {'node': 'node002', 'hardware': ['Dell Inc.', 'PowerEdge R650'],
         'components': [], 'differs': []}],
    'skipped': {'no inventory; has this node booted?': ['node003', 'node004'],
                'no catalogue entry for this hardware': ['node005']},
    'summary': ['1 node(s) would change, 1 already as the catalogue asks',
                '1 skipped: no catalogue entry for this hardware',
                '2 skipped: no inventory; has this node booted?']}}}}


@pytest.fixture
def wire(monkeypatch):
    """Captures what reaches the daemon, and what the terminal was shown."""
    seen = {'posted': [], 'fetched': [], 'tables': [], 'messages': []}

    import luna.firmwarecatalog as firmware

    monkeypatch.setattr(firmware.Rest, 'post_raw',
                        lambda self, uri, payload: seen['posted'].append(
                            {'uri': uri, 'payload': payload}) or FakeResponse(
                                payload={'message': 'firmware update queued for 1 node(s)',
                                         'request_id': 'abc123'}),
                        raising=False)
    monkeypatch.setattr(firmware.Rest, 'get_data',
                        lambda self, uri, *a, **k: seen['fetched'].append(uri) or
                        FakeResponse(payload=PREVIEW), raising=False)
    monkeypatch.setattr(firmware.Presenter, 'show_table',
                        lambda self, title, fields, rows: seen['tables'].append(
                            {'title': title, 'fields': fields, 'rows': rows}),
                        raising=False)
    for kind in ('show_success', 'show_warning', 'show_error'):
        monkeypatch.setattr(firmware.Message, kind,
                            lambda self, message, _kind=kind: seen['messages'].append(
                                (_kind, message)), raising=False)
    return seen


def push(table, **args):
    from luna.firmwarecatalog import firmware_push
    record = {'name': 'target', 'component': None, 'dry_run': None, 'raw': None}
    record.update(args)
    return firmware_push(table, record)


def test_a_real_push_posts_to_the_node_route(wire):
    push('node')
    assert [item['uri'] for item in wire['posted']] == ['config/node/target/_firmwarepush']
    assert wire['posted'][0]['payload'] == {'config': {'node': {'target': {}}}}
    assert wire['fetched'] == []


def test_a_named_component_travels_with_the_request(wire):
    push('node', component='BMC')
    assert wire['posted'][0]['payload']['config']['node']['target'] == {'component': 'BMC'}


def test_a_group_push_posts_to_the_group_route(wire):
    push('group')
    assert [item['uri'] for item in wire['posted']] == ['config/group/target/_firmwarepush']


def test_a_dry_run_records_nothing(wire):
    """The command an operator runs before deciding must not be the decision."""
    push('node', dry_run=True)
    assert wire['posted'] == []
    assert wire['fetched'] == ['node/target/firmware/_preview']


def test_a_dry_run_shows_a_row_per_component_that_would_change(wire):
    push('group', dry_run=True)
    rows = wire['tables'][0]['rows']
    assert [row[1:3] for row in rows] == [['node001', 'BMC'], ['node001', 'BIOS']]
    # a component nobody has ever reported is not a match, and says so
    assert rows[1][3] == 'unknown'
    assert rows[0][4] == '7.10'


def test_a_dry_run_groups_the_skips_by_cause_rather_than_listing_nodes(wire):
    """At four thousand nodes a line each buries what would actually change."""
    push('group', dry_run=True)
    warnings = [message for kind, message in wire['messages'] if kind == 'show_warning']
    assert warnings == ['1 node(s) skipped: no catalogue entry for this hardware',
                        '2 node(s) skipped: no inventory; has this node booted?']
    assert not any('node003' in message for _, message in wire['messages'])


def test_a_dry_run_filtered_to_one_component_leaves_the_others_out(wire):
    push('node', dry_run=True, component='BIOS')
    assert [row[2] for row in wire['tables'][0]['rows']] == ['BIOS']


def test_a_dry_run_that_would_change_nothing_says_so(wire, monkeypatch):
    import luna.firmwarecatalog as firmware
    nothing = {'config': {'firmware': {'preview': {
        'ready': [{'node': 'node001', 'differs': []}], 'skipped': {},
        'summary': ['0 node(s) would change, 1 already as the catalogue asks']}}}}
    monkeypatch.setattr(firmware.Rest, 'get_data',
                        lambda self, uri, *a, **k: FakeResponse(payload=nothing),
                        raising=False)
    push('node', dry_run=True)
    assert wire['tables'] == []
    assert ('show_success', 'Nothing would change.') in wire['messages']


STATUS = {'config': {'firmwarecatalog': {
    'status': {'node001': {'group': 'compute', 'component': 'BMC', 'request_id': 'r1',
                           'state': 'done', 'message': 'BMC now at the catalogue version',
                           'restore': 'pending', 'since': '2026-08-30'},
               'node002': {'group': 'compute', 'component': 'BMC', 'request_id': 'r1',
                           'state': 'done', 'message': 'BMC now at the catalogue version',
                           'restore': 'done: BMC answers; nothing to restore', 'since': '2026-08-30'}},
    'summary': {'done': 2}}}}


def status(wire, monkeypatch, **args):
    import luna.firmwarecatalog as firmware
    monkeypatch.setattr(firmware.Rest, 'get_data',
                        lambda self, uri, *a, **k: wire['fetched'].append(uri) or FakeResponse(payload=STATUS),
                        raising=False)
    record = {'action': 'status', 'name': None, 'group': None, 'raw': None, 'all': None, 'verbose': None}
    record.update(args)
    cmd = firmware.FirmwareCatalog.__new__(firmware.FirmwareCatalog)
    cmd.args, cmd.table, cmd.route = record, 'firmwarecatalog', 'firmwarecatalog'
    return cmd.status_firmwarecatalog()


def test_status_shows_the_restore_a_flash_owes_and_keeps_it_in_view_until_settled(wire, monkeypatch):
    """
    A BMC flash is not over when the flash is: the node still owes a restore. So the
    restore column is shown, and a done request with a pending restore still needs
    attention - hiding it with the done ones is how the admin learns of it from the board.
    """
    status(wire, monkeypatch)
    table = [t for t in wire['tables'] if t['fields'][0] == '#'][0]
    assert table['fields'][-1] == 'restore'
    assert [row[1] for row in table['rows']] == ['node001']
    assert table['rows'][0][-1] == 'pending'
    wire['tables'].clear()
    status(wire, monkeypatch, all=True)
    table = [t for t in wire['tables'] if t['fields'][0] == '#'][0]
    assert [row[-1] for row in table['rows']] == ['pending', 'done: BMC answers; nothing to restore']
