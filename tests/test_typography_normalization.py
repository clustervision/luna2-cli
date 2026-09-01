#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
Rich-text paste artefacts (curly quotes, non-breaking hyphens, ...) get
normalized to plain ASCII in comment/pre/part/postscript, but not content,
which is a byte-preserving path for binary secrets/profile files (TRIX-1868).
"""

import base64
import logging
from unittest.mock import patch

import pytest

import luna.utils.log as luna_log
from luna.utils.helper import Helper


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def test_the_exact_ticket_text_comes_back_ascii():
    text = "# Now it’s safe to wipe and re‑create everything"
    normalized, changed = Helper().normalize_typography(text)
    assert changed is True
    assert normalized == "# Now it's safe to wipe and re-create everything"
    assert all(ord(c) < 128 for c in normalized)


def test_plain_ascii_is_reported_unchanged():
    text = "echo hello world"
    normalized, changed = Helper().normalize_typography(text)
    assert changed is False
    assert normalized == text


@pytest.mark.parametrize('lookalike,ascii_equivalent', [
    ('‘single‘', "'single'"),
    ('“double”', '"double"'),
    ('en–dash', 'en-dash'),
    ('em—dash', 'em-dash'),
    ('non breaking space', 'non breaking space'),
    ('zero​width', 'zerowidth'),
    ('soft­hyphen', 'softhyphen'),
    ('ellipsis…', 'ellipsis...'),
])
def test_each_known_lookalike_is_rewritten(lookalike, ascii_equivalent):
    normalized, changed = Helper().normalize_typography(lookalike)
    assert changed is True
    assert normalized == ascii_equivalent


def test_base64_encode_text_normalizes_a_normalize_key_and_warns():
    with patch('luna.utils.helper.Message') as message:
        encoded = Helper().base64_encode_text('partscript', "it’s fine")
    assert base64.b64decode(encoded).decode('utf-8') == "it's fine"
    message.return_value.show_warning.assert_called_once()


def test_base64_encode_text_leaves_content_untouched_even_with_a_lookalike():
    """content is excluded from NORMALIZE_KEYS: a coincidental match must not be rewritten."""
    with patch('luna.utils.helper.Message') as message:
        encoded = Helper().base64_encode_text('content', "it’s fine")
    assert base64.b64decode(encoded).decode('utf-8') == "it’s fine"
    message.return_value.show_warning.assert_not_called()


def test_base64_encode_text_binary_content_still_round_trips():
    """Same byte-preservation guarantee test_content_encoding.py pins, for this choke point too."""
    binary = bytes([0x01, 0x02, 0xff, 0xfe, 0x00, 0x7f])
    with patch('luna.utils.helper.Message'):
        encoded = Helper().base64_encode_text('content', binary)
    assert base64.b64decode(encoded) == binary


def test_prepare_payload_normalizes_an_inline_quick_partscript_argument():
    """The exact reproduction from the ticket, via --quick-partscript."""
    text = "# Now it’s safe to re‑create everything"
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'partscript': text})
    decoded = base64.b64decode(payload['partscript']).decode('utf-8')
    assert decoded == "# Now it's safe to re-create everything"
    message.return_value.show_warning.assert_called_once()


def test_prepare_payload_does_not_touch_disklayout_text():
    """disklayout is machine syntax, not prose, and must skip normalization entirely."""
    layout = '{"version": 2, "sets": [{"role": "os", "devices": ["/dev/sda"], ' \
             '"volumes": ["/boot/efi", "/boot", "/"]}]}'
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'disklayout': layout})
    assert 'disklayout' in payload
    message.return_value.show_warning.assert_not_called()
