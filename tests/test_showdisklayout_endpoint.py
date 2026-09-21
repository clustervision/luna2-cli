#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
show_disklayout must read the dedicated /config/<table>/<name>/disklayout route
(which returns just the layout + _disklayout_source) rather than pulling the whole
node/group record. Pins the URL so a future refactor cannot quietly widen it back to
the full record.
"""

import base64
import json
from unittest.mock import MagicMock, patch

import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001



def _resp(table, name):
    layout = base64.b64encode(json.dumps({
        "version": 2,
        "sets": [{"name": "os", "role": "os", "selection": "discover", "raid": "none",
                  "volumes": [{"name": "root", "mountpoint": "/", "fs": "xfs",
                               "provider": "partition", "size": "100%"}]}],
    }).encode()).decode()
    return MagicMock(status_code=200, content={
        "config": {table: {name: {"disklayout": layout, "_disklayout_source": table}}}})


def test_showdisklayout_reads_the_narrow_disklayout_route():
    from luna.utils.helper import Helper
    with patch("luna.utils.helper.Rest") as rest, \
            patch("luna.utils.helper.Presenter"), patch("luna.utils.helper.Message"):
        rest.return_value.get_data.return_value = _resp("node", "n1")
        Helper().show_disklayout(table="node", args={"name": "n1", "raw": False})
    rest.return_value.get_data.assert_called_once_with("node", "n1/disklayout")


def test_showdisklayout_group_also_uses_the_narrow_route():
    from luna.utils.helper import Helper
    with patch("luna.utils.helper.Rest") as rest, \
            patch("luna.utils.helper.Presenter"), patch("luna.utils.helper.Message"):
        rest.return_value.get_data.return_value = _resp("group", "g1")
        Helper().show_disklayout(table="group", args={"name": "g1", "raw": False})
    rest.return_value.get_data.assert_called_once_with("group", "g1/disklayout")
