#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.
"""
TRIX-2097: a DNS entry name may carry several addresses. `dns add` appends, `dns change`
tells the daemon to replace, `dns remove` takes one address or the whole name.
"""
import logging

import pytest

from luna.utils import log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class Answer:
    def __init__(self, code):
        self.status_code, self.content = code, 'ok'


def _network(monkeypatch, args, seen):
    from luna.network import Network
    monkeypatch.setattr('luna.network.Rest', lambda: type('R', (), {
        'post_data': lambda self, table, name, data: seen.append(('post', name, data)) or Answer(201),
        'get_delete': lambda self, table, name: seen.append(('delete', name)) or Answer(204)})())
    monkeypatch.setattr('luna.network.Message', lambda: type('M', (), {
        'show_success': lambda self, *a: True, 'error_exit': lambda self, *a: (_ for _ in ()).throw(AssertionError(a))})())
    network = Network.__new__(Network)
    network.table, network.logger, network.args = 'network', logging.getLogger('luna2-cli-tests'), args
    return network


def test_add_sends_the_pair_and_change_sends_replace(monkeypatch):
    seen = []
    _network(monkeypatch, {'name': 'cluster', 'host': 'svc', 'ipaddress': '10.141.1.2'}, seen).network_dns_add()
    _network(monkeypatch, {'name': 'cluster', 'host': 'svc', 'ipaddress': '10.141.1.9'}, seen).network_dns_change()
    assert seen[0][2]['config']['dns']['cluster'] == [{'host': 'svc', 'ipaddress': '10.141.1.2'}]
    assert seen[1][2]['config']['dns']['cluster'] == [{'host': 'svc', 'ipaddress': '10.141.1.9', 'replace': True}]


def test_remove_names_the_address_when_given(monkeypatch):
    seen = []
    _network(monkeypatch, {'name': 'cluster', 'host': 'svc', 'ipaddress': '10.141.1.2'}, seen).network_dns_remove()
    _network(monkeypatch, {'name': 'cluster', 'host': 'svc', 'ipaddress': None}, seen).network_dns_remove()
    assert [s[1] for s in seen] == ['cluster/svc/10.141.1.2', 'cluster/svc']
