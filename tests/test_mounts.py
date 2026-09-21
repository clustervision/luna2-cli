#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
The mounts YAML/JSON front-end (TRIX-1651): terse YAML or JSON in, canonical JSON
out, with every scalar kept a string except the version.

The property that matters most is that `mode: 0755` and `mode: 1777` survive as
text. A YAML parser left to itself reads the first as octal 493 and the second as
1777 decimal, and either would silently change the mountpoint's permissions.
"""

import json

import pytest

from luna.utils.mounts import MountsError, SchemaVersion, canonicalize, to_yaml

YAML = """\
comment: cluster network mounts
mounts:
  - path: /trinity/home
    server: controller
    export:
      options: sync,no_subtree_check
      clients:
        - to: cluster
          options: rw,no_root_squash
        - to: 10.20.0.0/16
          options: ro
    options: nfsvers=4.2,rw,nconnect=16,_netdev,nofail
  - path: /trinity/scratch
    server: fileserver01
    owner: root
    group: users
    mode: 1777
  - path: /local/tmp
    type: manual
    mode: 0755
    state: present
"""


def _doc(raw):
    return json.loads(canonicalize(raw))


def test_yaml_canonicalizes_to_sorted_compact_json_with_the_version_filled():
    out = canonicalize(YAML)
    assert out == json.dumps(json.loads(out), sort_keys=True, separators=(",", ":")).encode()
    assert _doc(YAML)["version"] == SchemaVersion


def test_mode_and_everything_else_stays_text():
    mounts = _doc(YAML)["mounts"]
    assert mounts[1]["mode"] == "1777"
    assert mounts[2]["mode"] == "0755"
    assert mounts[2]["state"] == "present"
    assert mounts[0]["export"]["clients"][1]["to"] == "10.20.0.0/16"


def test_json_input_is_accepted_unchanged_in_meaning():
    doc = {"version": 1, "mounts": [{"path": "/a", "mode": "0755"}]}
    assert _doc(json.dumps(doc)) == doc


def test_a_numeric_mode_in_json_becomes_text_rather_than_a_number():
    # the daemon refuses a numeric mode; the front-end never manufactures one
    assert _doc('{"mounts": [{"path": "/a", "mode": 1777}]}')["mounts"][0]["mode"] == "1777"


def test_version_is_the_only_coerced_field():
    assert _doc("version: '1'\nmounts: []")["version"] == 1
    with pytest.raises(MountsError, match="version must be a whole number"):
        canonicalize("version: one\nmounts: []")


def test_empty_and_non_object_documents_are_refused_with_the_skeleton():
    with pytest.raises(MountsError, match="mounts document is empty"):
        canonicalize("")
    with pytest.raises(MountsError, match="must be an object"):
        canonicalize("- /trinity/home")


def test_yaml_sugar_is_refused():
    with pytest.raises(MountsError, match="duplicate key"):
        canonicalize("mounts: []\nmounts: []")
    with pytest.raises(MountsError, match="anchors and aliases"):
        canonicalize("a: &x [1]\nmounts: *x")


def test_bad_yaml_gets_a_plain_hint():
    with pytest.raises(MountsError, match="invalid YAML at line"):
        canonicalize("mounts:\n  - path /a\n    server: x: y")


def test_editor_round_trip_is_stable():
    stored = canonicalize(YAML)
    echoed = to_yaml(stored)
    assert canonicalize(echoed) == stored
    assert "mode: '1777'" in echoed or "mode: 1777" in echoed


def test_to_yaml_refuses_a_broken_stored_document():
    with pytest.raises(MountsError, match="not valid JSON"):
        to_yaml("{broken")
