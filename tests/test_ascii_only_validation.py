#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
comment/pre/part/postscript are rejected outright if they contain a non-ASCII
character (TRIX-1868), rather than silently rewritten - a curly quote or dash
pasted from Word must not be guessed at, since a replacement table can only
ever cover the lookalikes it was written for.
"""

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


def test_clean_ascii_text_passes():
    with patch('luna.utils.helper.Message') as message:
        Helper().check_ascii_only('partscript', "echo hello world")
    message.return_value.error_exit.assert_not_called()


def test_the_exact_ticket_text_is_rejected():
    text = "# Now it’s safe to wipe and re‑create everything"
    with patch('luna.utils.helper.Message') as message:
        Helper().check_ascii_only('partscript', text)
    error = message.return_value.error_exit.call_args.args[0]
    assert 'partscript' in error
    assert 'U+2019' in error
    assert 'U+2011' in error


def test_repeated_characters_are_counted_not_listed_individually():
    text = "a’b’c’"
    with patch('luna.utils.helper.Message') as message:
        Helper().check_ascii_only('comment', text)
    error = message.return_value.error_exit.call_args.args[0]
    assert '3 occurrences' in error


def test_bytes_input_is_decoded_first():
    with patch('luna.utils.helper.Message') as message:
        Helper().check_ascii_only('comment', "café".encode('utf-8'))
    error = message.return_value.error_exit.call_args.args[0]
    assert 'U+00E9' in error


def test_invalid_utf8_bytes_are_rejected_with_their_own_message():
    with patch('luna.utils.helper.Message') as message:
        Helper().check_ascii_only('comment', b'\xff\xfe')
    error = message.return_value.error_exit.call_args.args[0]
    assert 'not valid UTF-8' in error


def test_prepare_payload_rejects_an_inline_quick_partscript_argument():
    """The exact reproduction from the ticket, via --quick-partscript."""
    text = "# Now it’s safe to re‑create everything"
    with patch('luna.utils.helper.Message') as message:
        Helper().prepare_payload(None, {'name': 'n1', 'partscript': text})
    message.return_value.error_exit.assert_called_once()


def test_prepare_payload_leaves_content_untouched_even_with_special_chars():
    """content is excluded: it is the byte-preserving path for binary secrets/profile files."""
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'content': "it’s fine"})
    message.return_value.error_exit.assert_not_called()
    assert 'content' in payload


def test_prepare_payload_does_not_check_disklayout_text():
    layout = '{"version": 2, "sets": [{"role": "os", "devices": ["/dev/sda"], ' \
             '"volumes": ["/boot/efi", "/boot", "/"]}]}'
    with patch('luna.utils.helper.Message') as message:
        payload = Helper().prepare_payload(None, {'name': 'n1', 'disklayout': layout})
    message.return_value.error_exit.assert_not_called()
    assert 'disklayout' in payload
