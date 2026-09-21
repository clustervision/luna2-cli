"""TRIX-2001: luna node setupredfish asks the daemon to settle a node's Redfish accounts."""
import json
import logging

import pytest

import luna.utils.log as luna_log


class FakeResponse():
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.payload = payload if payload is not None else {}
        self.content = json.dumps(self.payload).encode()

    def json(self):
        return self.payload


@pytest.fixture
def sent(monkeypatch):
    posted = []
    import luna.node as node

    def fake_post_raw(self, uri, payload):
        posted.append({'uri': uri, 'payload': payload})
        return FakeResponse(payload={'request_id': None,
                                     'config': {'node': {'accounts': {'queued': 1}}}})
    monkeypatch.setattr(node.Rest, 'post_raw', fake_post_raw, raising=False)
    monkeypatch.setattr(node.Message, 'show_success', lambda self, *a, **k: None, raising=False)
    return posted


def node_with(args):
    from luna.node import Node
    instance = Node.__new__(Node)
    instance.logger = luna_log.Log.get_logger()
    instance.args = args
    instance.table = 'node'
    instance.table_cap = 'Node'
    return instance


def test_a_hostlist_goes_to_the_provision_route(sent):
    node_with({'name': 'node[001-004]', 'group': None}).setupredfish_node()
    assert sent == [{'uri': 'config/node/redfishaccounts/_provision',
                     'payload': {'config': {'node': {'hostlist': 'node[001-004]'}}}}]


def test_a_group_is_sent_as_a_group(sent):
    node_with({'name': None, 'group': 'compute'}).setupredfish_node()
    assert sent[0]['payload'] == {'config': {'node': {'group': 'compute'}}}
