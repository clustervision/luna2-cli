#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2229: the daemon accepts only ethernet and infiniband, in lower case, as a network type,
because those are the two the node interface templates know. add and change offer the same two.
"""

import argparse

import pytest

from luna.utils.arguments import Arguments


@pytest.fixture(params=[True, None], ids=['add', 'change'])
def parser(request):
    parser = argparse.ArgumentParser()
    Arguments().common_network_args(parser, request.param)
    return parser


def _parse(parser, value):
    return parser.parse_args(['-N', '10.0.0.0/16', '-t', value]).type


@pytest.mark.parametrize('value', ['ethernet', 'infiniband'])
def test_a_supported_type_is_taken(parser, value):
    assert _parse(parser, value) == value


@pytest.mark.parametrize('value', ['Ethernet', 'INFINIBAND', 'ethernt', 'ib'])
def test_any_other_type_is_refused_before_it_reaches_the_daemon(parser, value):
    with pytest.raises(SystemExit):
        _parse(parser, value)
