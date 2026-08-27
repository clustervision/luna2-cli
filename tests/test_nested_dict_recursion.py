#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
--raw on anything with a dictionary inside a dictionary.

Helper().nested_dict recursed on the dictionary it was handed rather than on the
nested value it had just found. The argument never got smaller, so it spun until
Python gave up: RecursionError, a screen of traceback, and no output.

It is reached from prepare_json, which is what every --raw goes through, so the
reproduction is any status view: 'luna profile status --raw' fails exactly the same
way and did so before any of this. Flat payloads never hit the branch, which is why
most of the CLI was fine and why it stayed unnoticed.

Both halves are asserted here - that it terminates, and that it returns the whole
structure rather than the first key of it, since the branch used to return early.
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


def test_a_dictionary_inside_a_dictionary_terminates():
    """The crash itself. Two levels is all it took."""
    assert Helper().nested_dict({'status': {'node001': {'state': 'matched'}}}) == {
        'status': {'node001': {'state': 'matched'}}}


def test_every_key_survives_not_just_the_first():
    """
    The branch used to `return` on the first nested dictionary, so even without the
    recursion a sibling key after it would have been dropped. A status payload is
    exactly that shape: the rows, and then the summary.
    """
    payload = {
        'status': {'node001': {'state': 'matched'}, 'node002': {'state': 'drifted'}},
        'summary': {'matched': 1, 'drifted': 1},
    }
    result = Helper().nested_dict(payload)
    assert set(result) == {'status', 'summary'}
    assert result['summary'] == {'matched': 1, 'drifted': 1}
    assert set(result['status']) == {'node001', 'node002'}


@pytest.mark.parametrize('depth', [1, 2, 5, 20])
def test_it_goes_as_deep_as_it_is_given(depth):
    payload = value = {}
    for level in range(depth):
        value['down'] = {'level': str(level)}
        value = value['down']
    assert Helper().nested_dict(payload) == payload


def test_a_flat_dictionary_is_unchanged():
    """The path most of the CLI takes, which was never broken and must stay that way."""
    flat = {'name': 'node001', 'state': 'matched', 'count': 3, 'nothing': None}
    assert Helper().nested_dict(dict(flat)) == flat


def test_prepare_json_reaches_it_the_way_every_raw_flag_does():
    """
    prepare_json is what --raw calls, and it hands the nested value down correctly -
    which is what made the bug one level lower so easy to miss.
    """
    payload = {'config': {'biosconfig': {
        'status': {'node001': {'state': 'matched', 'config': 'hpc-tuned'}},
        'summary': {'matched': 1}}}}
    result = Helper().prepare_json(payload)
    assert result['config']['biosconfig']['summary'] == {'matched': 1}
    assert result['config']['biosconfig']['status']['node001']['config'] == 'hpc-tuned'
