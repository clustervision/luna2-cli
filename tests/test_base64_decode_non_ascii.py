#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
'luna node show' on a script containing a curly quote (TRIX-1868).

Someone pasted Word/Outlook text into a partscript. Word substitutes typographic
lookalikes for the ASCII original as you type - here, U+2019 RIGHT SINGLE
QUOTATION MARK for a straight apostrophe. Luna stores that fine (it is valid
UTF-8), but showing it back calls Helper().base64_decode() on the stored value,
which - for reasons explained in show_data() and TRIX-1868 - is sometimes handed
plain, already-decoded text rather than actual base64.

base64.b64decode(..., validate=True) starts by doing content.encode('ascii'),
which fails for that curly quote. base64 catches the UnicodeEncodeError itself
and re-raises it as a plain ValueError('string argument should contain only
ASCII characters') - not the UnicodeEncodeError you would expect - and
base64_decode only caught binascii.Error (also a ValueError, but a different
subclass) and UnicodeDecodeError. Neither matched, so the exception reached the
CLI's top level and 'luna node show' died instead of printing the record.

The fix is a plain `except ValueError`, which also covers binascii.Error since
that is itself a ValueError subclass.
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
    """The pre-existing behaviour this must not regress: invalid-but-ASCII text
    (the common case, since prepare_json can run the decode step twice - see
    show_data()) already came back unchanged via the binascii.Error branch."""
    text = "not valid base64 either"
    assert Helper().base64_decode(text) == text


def test_actual_base64_still_decodes():
    """The happy path must keep working: real stored content still decodes."""
    import base64
    encoded = base64.b64encode("hello world".encode("utf-8")).decode("ascii")
    assert Helper().base64_decode(encoded) == "hello world"


def test_none_passes_through():
    assert Helper().base64_decode(None) is None
