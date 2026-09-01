#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
base64_decode() must not crash on non-ASCII text (TRIX-1868): a pasted curly
quote made b64decode raise ValueError, which the old except clauses missed.
"""

import logging

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


def test_a_curly_quote_does_not_crash_the_decode():
    """The exact character from the ticket: U+2019 in an otherwise plain comment."""
    text = "# Now it’s safe to wipe and re‑create everything"
    assert Helper().base64_decode(text) == text


def test_plain_ascii_text_that_is_not_base64_is_unaffected():
    """Pre-existing behaviour: invalid-but-ASCII text already came back unchanged."""
    text = "not valid base64 either"
    assert Helper().base64_decode(text) == text


def test_actual_base64_still_decodes():
    """The happy path must keep working: real stored content still decodes."""
    import base64
    encoded = base64.b64encode("hello world".encode("utf-8")).decode("ascii")
    assert Helper().base64_decode(encoded) == "hello world"


def test_none_passes_through():
    assert Helper().base64_decode(None) is None
