#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.

"""TRIX-1969: a profile's enabled flag has only true and false states."""

import argparse
import logging

import pytest

import luna.utils.log as luna_log
from luna.profile import Profile


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


def _parser():
    parser = argparse.ArgumentParser(prog='luna')
    subparsers = parser.add_subparsers(dest='table')
    Profile(parser=parser, subparsers=subparsers)
    return parser


def test_profile_enabled_help_offers_only_two_states():
    enabled = next(action for action in
                   _parser()._subparsers._group_actions[0].choices['profile']
                   ._subparsers._group_actions[0].choices['change']._actions
                   if action.dest == 'enabled')
    assert enabled.choices == ['y', 'yes', 'n', 'no']


def test_profile_enabled_rejects_an_empty_value():
    with pytest.raises(SystemExit):
        _parser().parse_args(['profile', 'change', 'p', '--enabled', ''])


@pytest.mark.parametrize(('value', 'expected'), [
    ('y', True), ('yes', True), ('n', False), ('no', False),
])
def test_profile_enabled_payload_is_boolean(value, expected):
    profile = Profile.__new__(Profile)
    profile.args = {'enabled': value}
    assert profile.profile_payload() == {'enabled': expected}
