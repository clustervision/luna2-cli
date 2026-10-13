#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""A swap volume on a RAID set gets provider lvm: the node refuses a direct
partition volume on raid ("direct partition volumes require raid=none"), so a
raid os set with a short-form swap was stored and then parked at install."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

_MOD_PATH = Path(__file__).resolve().parent.parent / "luna" / "utils" / "disklayout.py"
_spec = importlib.util.spec_from_file_location("luna_disklayout_swap_raid", _MOD_PATH)
disklayout = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disklayout)


def _volumes(yaml_text: str) -> list[dict]:
    doc = json.loads(disklayout.canonicalize(yaml_text))
    return doc["sets"][0]["volumes"]


def test_swap_on_a_raid_set_is_lvm() -> None:
    v = _volumes("role: os\nraid: 1\ndevices: [/dev/vda, /dev/vdb]\nvolumes: [[swap, 8G]]\n")[0]
    assert v["mountpoint"] == "swap" and v["provider"] == "lvm"


def test_swap_without_raid_stays_a_partition() -> None:
    v = _volumes("role: data\ndevices: [/dev/vdb]\nvolumes: [[swap, 8G]]\n")[0]
    assert v["provider"] == "partition"


def test_an_explicit_provider_is_kept() -> None:
    doc = {"version": 2, "sets": [{"name": "os", "role": "os", "raid": "1", "devices": ["/dev/vda", "/dev/vdb"],
                                   "volumes": [{"mountpoint": "swap", "size": "8G", "provider": "partition"}]}]}
    v = json.loads(disklayout.canonicalize(json.dumps(doc)))["sets"][0]["volumes"][0]
    assert v["provider"] == "partition"
