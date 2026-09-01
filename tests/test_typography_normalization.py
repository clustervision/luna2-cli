#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
Rich-text paste artefacts in comment/pre/part/postscript (TRIX-1868).

Word, Outlook and most browsers substitute a curly quote, a non-breaking
hyphen, an en/em dash, ... for the plain ASCII original as you type - the two
look identical in an editor. Stored verbatim, one of these used to crash
'luna node show' outright (see test_base64_decode_non_ascii.py and
test_show_data_single_decode.py); left inside an actual script rather than a
comment, it is worse, because a POSIX shell does not recognise a curly quote
as a quote at all - DISK="/dev/sda" typed with curly double quotes just sets
DISK to a literal string containing three extra bytes.

normalize_typography() rewrites the known lookalikes to their ASCII original.
base64_encode_text() is the single choke point that applies it: the inline
--quick-* argument path (prepare_payload) and the interactive editor path
(open_editor) both go through it, for exactly the free-text keys named in
NORMALIZE_KEYS. content is deliberately NOT one of them - it is a
byte-preserving path for binary secrets and profile files
(test_content_encoding.py), and a coincidental codepoint match in binary data
must not be corrupted by this.
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
    """content is excluded from NORMALIZE_KEYS on purpose: it is the
    byte-preserving path used for binary secrets and profile files, and a
    coincidental match must not be rewritten."""
    with patch('luna.utils.helper.Message') as message:
        encoded = Helper().base64_encode_text('content', "it’s fine")
    assert base64.b64decode(encoded).decode('utf-8') == "it’s fine"
    message.return_value.show_warning.assert_not_called()


def test_base64_encode_text_binary_content_still_round_trips():
    """The same byte-preservation guarantee test_content_encoding.py pins for
    Profile.file_content must hold for the shared choke point too."""
    binary = bytes([0x01, 0x02, 0xff, 0xfe, 0x00, 0x7f])
    with patch('luna.utils.helper.Message'):
        encoded = Helper().base64_encode_text('content', binary)
    assert base64.b64decode(encoded) == binary


def test_prepare_payload_normalizes_an_inline_quick_partscript_argument():
    """The exact reproduction from the ticket: --quick-partscript on the
    command line with a Word-pasted apostrophe and non-breaking hyphen."""
    text = "# Now it’s safe to re‑create everything"
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'partscript': text})
    decoded = base64.b64decode(payload['partscript']).decode('utf-8')
    assert decoded == "# Now it's safe to re-create everything"
    message.return_value.show_warning.assert_called_once()


def test_prepare_payload_does_not_touch_disklayout_text():
    """disklayout is machine syntax (JSON/YAML), not prose a paste artefact
    would land in, and it has its own canonicalizing encoder (disklayout_b64).
    It must not go through typography normalization at all."""
    layout = '{"version": 2, "sets": [{"role": "os", "devices": ["/dev/sda"], ' \
             '"volumes": ["/boot/efi", "/boot", "/"]}]}'
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'disklayout': layout})
    assert 'disklayout' in payload
    message.return_value.show_warning.assert_not_called()
