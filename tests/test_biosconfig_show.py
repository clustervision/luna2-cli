#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2162: `luna biosconfig show -s` lists each setting with the name the board
gives it. The attribute stays in the first column and in -R untouched, because
it is what --set, a push and a script key on; the name is for reading only and
is left empty where the daemon has none.
"""

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


def record(labels=None):
    detail = {'name': 'golden', 'manufacturer': 'GIGABYTE', 'model': 'R181-Z91-00',
              'biosversion': 'F25', 'grabbedfrom': 'node001', 'settings': 2,
              'grab_exclude': '', 'updated': '2026-09-23 10:00:00', 'comment': None,
              'attributes': {'PCIS003': 'Enabled', 'Naples0265': 'Last State'}}
    if labels is not None:
        detail['labels'] = labels
    return {'config': {'biosconfig': {'golden': detail}}}


@pytest.fixture
def wire(monkeypatch):
    """Serves one configuration and captures what the terminal was shown."""
    seen = {'tables': [], 'json': [], 'payload': None}
    import luna.biosconfig as bios
    monkeypatch.setattr(bios.Rest, 'get_data',
                        lambda self, table, name, *a, **k: FakeResponse(payload=seen['payload']),
                        raising=False)
    monkeypatch.setattr(bios.Presenter, 'show_table',
                        lambda self, title, fields, rows: seen['tables'].append(
                            {'fields': fields, 'rows': rows}), raising=False)
    monkeypatch.setattr(bios.Presenter, 'show_table_col',
                        lambda self, title, fields, rows: None, raising=False)
    monkeypatch.setattr(bios.Presenter, 'show_json',
                        lambda self, data: seen['json'].append(data), raising=False)
    return seen


def show(**args):
    from luna.biosconfig import BiosConfig
    command = BiosConfig.__new__(BiosConfig)
    command.table = 'biosconfig'
    command.args = dict({'name': 'golden', 'settings': True, 'raw': None}, **args)
    return command.show_biosconfig()


def test_each_setting_shows_its_attribute_its_name_and_its_value(wire):
    wire['payload'] = record(labels={'PCIS003': 'Above 4G Decoding'})
    show()
    table = wire['tables'][0]
    assert table['fields'] == ['Attribute', 'Name', 'Value']
    assert table['rows'] == [['Naples0265', '', 'Last State'],
                             ['PCIS003', 'Above 4G Decoding', 'Enabled']]


def test_a_daemon_that_sends_no_labels_still_shows_every_setting(wire):
    wire['payload'] = record()
    show()
    assert wire['tables'][0]['rows'] == [['Naples0265', '', 'Last State'],
                                         ['PCIS003', '', 'Enabled']]


def test_raw_keeps_the_attributes_as_they_are_and_adds_the_labels_beside_them(wire):
    wire['payload'] = record(labels={'PCIS003': 'Above 4G Decoding'})
    show(raw=True)
    shown = wire['json'][0]
    assert shown['attributes'] == {'PCIS003': 'Enabled', 'Naples0265': 'Last State'}
    assert shown['labels'] == {'PCIS003': 'Above 4G Decoding'}
