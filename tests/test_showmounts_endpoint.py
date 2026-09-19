#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
show_mounts reads the narrow /config/<table>[/<name>]/mounts route rather than
the whole record, for the cluster as well as a group or a node, and the show
path summarises a stored document to one line rather than a truncated JSON blob.
Pins the URLs so a refactor cannot quietly widen them back to the full record.
"""

import base64
import json
import logging
from unittest.mock import MagicMock, patch

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


DOC = {"version": 1, "mounts": [
    {"path": "/trinity/home", "server": "controller",
     "export": {"clients": [{"to": "cluster", "options": "rw"}]}},
    {"path": "/local/tmp", "type": "manual"},
]}
B64 = base64.b64encode(json.dumps(DOC).encode()).decode()


def _resp(table, name, source):
    entry = {"mounts": B64, "_mounts_source": source}
    body = {table: {name: entry}} if name else {table: entry}
    return MagicMock(status_code=200, content={"config": body})


@pytest.mark.parametrize('table,name,uri', [
    ('node', 'n1', 'n1/mounts'),
    ('group', 'g1', 'g1/mounts'),
    ('cluster', None, 'mounts'),
])
def test_showmounts_reads_the_narrow_route(table, name, uri):
    from luna.utils.helper import Helper
    args = {'raw': False}
    if name:
        args['name'] = name
    with patch("luna.utils.helper.Rest") as rest, \
            patch("luna.utils.helper.Presenter") as presenter, patch("luna.utils.helper.Message"):
        rest.return_value.get_data.return_value = _resp(table, name, 'cluster')
        Helper().show_mounts(table=table, args=args)
    rest.return_value.get_data.assert_called_once_with(table, uri)
    title, fields, rows = presenter.return_value.show_table.call_args.args
    assert '[from cluster]' in title
    assert fields[0] == 'Path'
    assert [row[0] for row in rows] == ['/trinity/home', '/local/tmp']
    assert rows[0][-1] == 'cluster(rw)' and rows[1][-1] == '-'


def test_showmounts_raw_prints_the_document():
    from luna.utils.helper import Helper
    with patch("luna.utils.helper.Rest") as rest, \
            patch("luna.utils.helper.Presenter") as presenter, patch("luna.utils.helper.Message"):
        rest.return_value.get_data.return_value = _resp('node', 'n1', 'node')
        Helper().show_mounts(table='node', args={'name': 'n1', 'raw': True})
    presenter.return_value.show_json.assert_called_once()
    presenter.return_value.show_table.assert_not_called()


def test_no_document_is_a_warning_not_an_error():
    from luna.utils.helper import Helper
    empty = MagicMock(status_code=200, content={"config": {"node": {"n1": {
        "mounts": base64.b64encode(b'').decode(), "_mounts_source": "default"}}}})
    with patch("luna.utils.helper.Rest") as rest, \
            patch("luna.utils.helper.Presenter") as presenter, patch("luna.utils.helper.Message") as message:
        rest.return_value.get_data.return_value = empty
        Helper().show_mounts(table='node', args={'name': 'n1', 'raw': False})
    message.return_value.show_warning.assert_called_once()
    presenter.return_value.show_table.assert_not_called()


def test_brief_mounts_is_one_line_and_never_raises():
    from luna.utils.helper import Helper
    assert Helper().brief_mounts(json.dumps(DOC)) == '2 mounts: /trinity/home, /local/tmp'
    assert Helper().brief_mounts('{"version": 1, "mounts": []}') == 'no mounts'
    assert Helper().brief_mounts('{broken').startswith('<unreadable mounts JSON')
    assert Helper().brief_mounts('') == ''
