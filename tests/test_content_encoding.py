#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.

"""
Content given on the command line has to survive being bytes.

Python decodes argv with surrogateescape, so a byte that is not valid UTF-8 arrives as
a lone surrogate. Encoding that back with bytes(text, 'utf-8') raises, and the operator
sees a traceback instead of a message - for the ordinary case of a key, a certificate,
or any other file that is not text.

Re-encoding the same way it was decoded gives back exactly the bytes the shell passed.
"""

import base64
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give the CLI a logger without Log.init_log()'s root-only file handler -
    the same shape the disklayout tests use."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


BINARY = bytes([0x01, 0x02, 0xff, 0xfe, 0x00, 0x7f])


def _as_argv(raw: bytes) -> str:
    """What Python hands the CLI for these bytes on the command line."""
    return raw.decode('utf-8', 'surrogateescape')


def test_binary_content_from_the_command_line_round_trips():
    from luna.profile import Profile
    encoded = Profile.file_content(Profile.__new__(Profile), _as_argv(BINARY))
    assert base64.b64decode(encoded) == BINARY


def test_plain_text_is_unaffected():
    from luna.profile import Profile
    encoded = Profile.file_content(Profile.__new__(Profile), 'pool ntp.example.org iburst')
    assert base64.b64decode(encoded) == b'pool ntp.example.org iburst'


def test_utf8_text_survives_as_utf8():
    """A UTF-8 name or comment must not be mangled by the byte-preserving path."""
    from luna.profile import Profile
    text = 'süß — ünïcode'
    encoded = Profile.file_content(Profile.__new__(Profile), text)
    assert base64.b64decode(encoded).decode('utf-8') == text


def test_the_old_encoding_would_have_raised():
    """Pins why the call site is written the way it is: the obvious form fails on
    exactly the input this test exists for."""
    with pytest.raises(UnicodeEncodeError):
        bytes(_as_argv(BINARY), 'utf-8')
