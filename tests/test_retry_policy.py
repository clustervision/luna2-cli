#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2049: the client must not retry a daemon that is merely slow.

A read timeout means the connection was made and the request landed - the daemon
has simply not answered yet. Retrying it repeats a control action that is not
idempotent, and it puts the retries on a daemon that is by definition already
slow, which is the opposite of backing off. Measured on the test pair: six API
workers, and one command against a dead BMC could put up to seven requests on
them by itself.

A failed connection is the opposite case: nothing was delivered, so it is still
worth retrying.
"""

import logging

import pytest
import urllib3
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, ReadTimeoutError

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def policy(monkeypatch):
    """The retry policy Rest() actually mounts, without needing a daemon."""
    from luna.utils.rest import Rest
    monkeypatch.setattr(Rest, 'get_ini_info',
                        lambda self: ('u', 'p', 'https://daemon:7050', 'k', 'no'))
    return Rest().retries


def test_a_read_timeout_is_not_retried(monkeypatch):
    """The defect: total=6 alone retried a slow daemon up to six more times."""
    retries = policy(monkeypatch)
    assert retries.read == 0
    with pytest.raises(MaxRetryError):
        retries.increment(method='GET', url='/x',
                          error=ReadTimeoutError(None, '/x', 'read timed out'))


def test_a_failed_connection_is_still_retried(monkeypatch):
    """The other half: nothing was delivered, so retrying is right."""
    retries = policy(monkeypatch)
    nxt = retries.increment(method='GET', url='/x', error=ConnectTimeoutError(None, '/x'))
    assert nxt.connect == retries.connect - 1


def test_a_502_is_still_retried(monkeypatch):
    """A daemon that answered with a gateway error has not done the work."""
    retries = policy(monkeypatch)
    assert 502 in retries.status_forcelist
    assert retries.status and retries.status > 0
