#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
show_data() must decode a stored record exactly once (TRIX-1868): it used to
run an already-decoded record back through prepare_json(), which could crash
on a pasted character or silently re-decode plaintext that looked like base64.
"""

import base64
import logging
from unittest.mock import MagicMock, patch

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _node_response(partscript_plain):
    stored = base64.b64encode(partscript_plain.encode('utf-8')).decode('ascii')
    return MagicMock(status_code=200, content={
        'config': {'node': {'n1': {'name': 'n1', 'partscript': stored}}}})


def test_a_pasted_curly_quote_does_not_crash_show():
    """The exact reproduction from the ticket: must print, not raise."""
    from luna.utils.helper import Helper
    text = "# Now it’s safe to wipe and re‑create everything"
    with patch('luna.utils.helper.Rest') as rest, \
            patch('luna.utils.helper.Presenter') as presenter, \
            patch('luna.utils.helper.Message'):
        rest.return_value.get_data.return_value = _node_response(text)
        Helper().show_data(table='node', args={'name': 'n1', 'raw': False})
    rows = presenter.return_value.show_table_col.call_args.args[2]
    assert text in rows


def test_plain_text_that_is_also_valid_base64_is_not_decoded_twice():
    """'aGVsbG8=' must come back unchanged, not silently decoded again into 'hello'."""
    from luna.utils.helper import Helper
    lookalike = "aGVsbG8="
    with patch('luna.utils.helper.Rest') as rest, \
            patch('luna.utils.helper.Presenter') as presenter, \
            patch('luna.utils.helper.Message'):
        rest.return_value.get_data.return_value = _node_response(lookalike)
        Helper().show_data(table='node', args={'name': 'n1', 'raw': False})
    rows = presenter.return_value.show_table_col.call_args.args[2]
    assert lookalike in rows
    assert 'hello' not in rows


def test_a_long_script_is_still_length_limited():
    """limit_content() must still trim a long script for the default (non -f) view."""
    from luna.utils.helper import Helper
    text = '\n'.join(f'line {i}' for i in range(10))
    with patch('luna.utils.helper.Rest') as rest, \
            patch('luna.utils.helper.Presenter') as presenter, \
            patch('luna.utils.helper.Message'):
        rest.return_value.get_data.return_value = _node_response(text)
        Helper().show_data(table='node', args={'name': 'n1', 'raw': False})
    rows = presenter.return_value.show_table_col.call_args.args[2]
    trimmed = next(row for row in rows if isinstance(row, str) and row.startswith('line 0'))
    assert 'More lines...' in trimmed
    assert 'line 9' not in trimmed
