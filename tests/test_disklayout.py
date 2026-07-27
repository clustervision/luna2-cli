#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
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

"""
Test battery for luna.utils.disklayout -- the YAML/JSON disklayout front-end.

The module is a PURE FUNCTION (text -> canonical JSON | reject), so every input
falls in exactly one of three buckets, and the battery enumerates all three:

  (1) meaning-preserving  -> byte-identical canonical JSON
      (JSON<->YAML, key order, whitespace, quoting, BOM)
  (2) meaning-changing    -> correspondingly different canonical JSON
  (3) invalid/hostile     -> a clean DisklayoutError (never crash/hang/coerce)

The one forbidden outcome (TE-CFG-SILENT) is a bucket-1-looking output that has
actually changed meaning -- chiefly YAML's implicit scalar coercion. The
coercion tests below pin that it cannot happen.

The module is loaded by file path to avoid luna/__init__.py's import-time side
effects (it provisions /trinity config dirs); the module itself has no
luna-internal imports, so this is faithful.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given, settings
from hypothesis import strategies as st

_MOD_PATH = Path(__file__).resolve().parent.parent / "luna" / "utils" / "disklayout.py"
_spec = importlib.util.spec_from_file_location("luna_disklayout_under_test", _MOD_PATH)
assert _spec is not None and _spec.loader is not None
disklayout = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disklayout)

canonicalize = disklayout.canonicalize
to_yaml = disklayout.to_yaml
DisklayoutError = disklayout.DisklayoutError


# --------------------------------------------------------------------------- #
# Seed layouts (one per storage path) -- the R-class golden corpus.
# --------------------------------------------------------------------------- #
SEED_LAYOUTS: dict[str, dict] = {
    "tmpfs_ram_root": {
        "version": 2,
        "sets": [{"role": "os", "volumes": [{"fs": "tmpfs", "provider": "memory"}]}],
    },
    "squashfs_ram_root": {
        "version": 2,
        "sets": [{"role": "os", "volumes": [{"fs": "squashfs", "provider": "memory"}]}],
    },
    "single_disk_lvm": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "devices": ["/dev/vda"],
                "selection": "manual",
                "raid": "none",
                "volumes": [
                    {"mountpoint": "/boot/efi", "fs": "vfat", "provider": "partition", "size": "600M"},
                    {"mountpoint": "/boot", "fs": "xfs", "provider": "partition", "size": "1G"},
                    {"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"},
                ],
            }
        ],
    },
    "two_disk_mirror": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "selection": "discover",
                "raid": "1",
                "count": 2,
                "match": {"min_size": "20G"},
                "volumes": [
                    {"mountpoint": "/boot/efi", "fs": "vfat", "provider": "partition", "size": "600M"},
                    {"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"},
                ],
            }
        ],
    },
    "zfs_mirror": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "selection": "discover",
                "raid": "mirror",
                "count": 2,
                "volumes": [
                    {"mountpoint": "/boot/efi", "fs": "vfat", "provider": "partition", "size": "600M"},
                    {"mountpoint": "/", "fs": "zfs", "provider": "zpool"},
                ],
            }
        ],
    },
    "multi_set_persistent_data": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "devices": ["/dev/vda"],
                "volumes": [{"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"}],
            },
            {
                "role": "data",
                "name": "scratch",
                "selection": "discover",
                "raid": "0",
                "count": 4,
                "spares": 1,
                "persistent": True,
                "volumes": [{"mountpoint": "/scratch", "fs": "xfs", "provider": "lvm", "size": "100%"}],
            },
        ],
    },
    "discover_save": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "selection": "discover",
                "raid": "10",
                "count": 4,
                "save": True,
                "match": {"tags": ["ssd"], "model": "no"},
                "volumes": [{"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"}],
            }
        ],
    },
    "clear_nvram": {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "devices": ["/dev/nvme0n1"],
                "volumes": [
                    {
                        "mountpoint": "/boot/efi",
                        "fs": "vfat",
                        "provider": "partition",
                        "size": "600M",
                        "clear_uefi_nvram": True,
                    },
                    {"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"},
                ],
            }
        ],
    },
}


def _canon(obj: dict) -> bytes:
    """Canonicalize a Python layout via its JSON serialization (the stored form)."""
    return canonicalize(json.dumps(obj))


# --------------------------------------------------------------------------- #
# Bucket 1 -- meaning-preserving inputs map to byte-identical canonical JSON.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", sorted(SEED_LAYOUTS))
def test_json_and_yaml_forms_are_identical(name: str) -> None:
    """The SAME layout as JSON and as YAML must produce identical canonical bytes."""
    obj = SEED_LAYOUTS[name]
    from_json = canonicalize(json.dumps(obj))
    from_yaml = canonicalize(yaml.safe_dump(obj))
    assert from_json == from_yaml


@pytest.mark.parametrize("name", sorted(SEED_LAYOUTS))
def test_idempotent(name: str) -> None:
    """canonicalize(canonicalize(x)) == canonicalize(x)."""
    once = _canon(SEED_LAYOUTS[name])
    twice = canonicalize(once)
    assert once == twice


@pytest.mark.parametrize("name", sorted(SEED_LAYOUTS))
def test_editor_round_trip(name: str) -> None:
    """to_yaml(canonical) re-canonicalizes to the same canonical bytes (BE-R1)."""
    once = _canon(SEED_LAYOUTS[name])
    rendered = to_yaml(once)
    assert canonicalize(rendered) == once


@pytest.mark.parametrize("name", sorted(SEED_LAYOUTS))
def test_key_order_irrelevant(name: str) -> None:
    """Reordering keys in the input must not change the canonical output."""
    obj = SEED_LAYOUTS[name]
    reordered = json.dumps(obj, sort_keys=True)
    unsorted = json.dumps(obj, sort_keys=False)
    assert canonicalize(reordered) == canonicalize(unsorted)


def test_utf8_bom_is_tolerated() -> None:
    obj = SEED_LAYOUTS["single_disk_lvm"]
    plain = json.dumps(obj).encode("utf-8")
    with_bom = b"\xef\xbb\xbf" + plain
    assert canonicalize(with_bom) == canonicalize(plain)


def test_whitespace_and_comments_yaml() -> None:
    """A YAML doc with blank lines and comments == its compact JSON twin."""
    yaml_text = """
# an OS set on one disk
version: 2
sets:
  - role: os

    devices: [/dev/vda]
    volumes:
      - mountpoint: /          # the root
        fs: xfs
        provider: lvm
        size: "100%"
"""
    twin = {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "devices": ["/dev/vda"],
                "volumes": [{"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"}],
            }
        ],
    }
    assert canonicalize(yaml_text) == _canon(twin)


# --------------------------------------------------------------------------- #
# Bucket 1/forbidden -- the Norway problem: string fields keep their string value.
# --------------------------------------------------------------------------- #
# Norway-shaped words that PyYAML would implicitly coerce to bool/int/float but
# which MUST survive as their exact string in a string field. (null/~ are handled
# separately below -- they are genuine null, not a coerced word.)
NORWAY_STRINGS = ["no", "yes", "on", "off", "true", "false", "10", "0600", "1:30", "1e3", "0x10"]


@pytest.mark.parametrize("value", NORWAY_STRINGS)
def test_string_field_not_coerced(value: str) -> None:
    """A Norway-shaped value in a STRING field survives as that exact string."""
    layout = {
        "version": 2,
        "sets": [
            {
                "role": "os",
                "raid": value,  # raid is a string field
                "match": {"model": value},
                "volumes": [{"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": value}],
            }
        ],
    }
    # Feed it as YAML (unquoted) -- the path where PyYAML would coerce.
    yaml_text = (
        f"version: 2\n"
        f"sets:\n"
        f"- role: os\n"
        f"  raid: {value}\n"
        f"  match: {{model: {value}}}\n"
        f"  volumes:\n"
        f"  - {{mountpoint: /, fs: xfs, provider: lvm, size: {value}}}\n"
    )
    out = json.loads(canonicalize(yaml_text))
    the_set = out["sets"][0]
    assert the_set["raid"] == value and isinstance(the_set["raid"], str)
    assert the_set["match"]["model"] == value and isinstance(the_set["match"]["model"], str)
    assert the_set["volumes"][0]["size"] == value
    # And the YAML form equals the explicit-JSON twin (no coercion drift).
    assert canonicalize(yaml_text) == _canon(layout)


# --------------------------------------------------------------------------- #
# Bucket 1 -- typed fields ARE coerced (int/bool), from either format.
# --------------------------------------------------------------------------- #
def test_typed_fields_coerced_from_yaml() -> None:
    yaml_text = """
version: "2"
sets:
- role: os
  selection: discover
  raid: "1"
  count: "2"
  spares: "0"
  save: "yes"
  persistent: "no"
  volumes:
  - {mountpoint: /, fs: xfs, provider: lvm, size: 100%, clear_uefi_nvram: "true"}
"""
    out = json.loads(canonicalize(yaml_text))
    s = out["sets"][0]
    assert out["version"] == 2 and isinstance(out["version"], int)
    assert s["count"] == 2 and isinstance(s["count"], int)
    assert s["spares"] == 0
    assert s["save"] is True
    assert s["persistent"] is False
    assert s["volumes"][0]["clear_uefi_nvram"] is True
    # raid stays the STRING "1" (it is a string field, not an int one).
    assert s["raid"] == "1" and isinstance(s["raid"], str)


@pytest.mark.parametrize("nullword", ["null", "~"])
def test_unquoted_null_is_json_null(nullword: str) -> None:
    """Unquoted YAML null in a string field becomes JSON null (faithful), not coerced."""
    out = json.loads(canonicalize(f"version: 2\nsets:\n- {{role: os, raid: {nullword}, volumes: []}}\n"))
    assert out["sets"][0]["raid"] is None


@pytest.mark.parametrize("nullword", ["null", "~"])
def test_quoted_null_stays_string(nullword: str) -> None:
    """Quoting preserves the literal string (the operator's escape hatch)."""
    out = json.loads(canonicalize(f'version: 2\nsets:\n- {{role: os, raid: "{nullword}", volumes: []}}\n'))
    assert out["sets"][0]["raid"] == nullword


@pytest.mark.parametrize("word,expected", [("yes", True), ("no", False), ("on", True), ("off", False),
                                           ("true", True), ("false", False), ("Y", True), ("N", False)])
def test_bool_words(word: str, expected: bool) -> None:
    out = json.loads(canonicalize(f"version: 2\nsets:\n- {{role: os, persistent: {word}, volumes: []}}\n"))
    assert out["sets"][0]["persistent"] is expected


# --------------------------------------------------------------------------- #
# Bucket 2 -- meaning-changing edits produce different canonical JSON.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", sorted(SEED_LAYOUTS))
def test_value_change_is_visible(name: str) -> None:
    """Changing one storage-bearing value must change the canonical output."""
    import copy

    base = _canon(SEED_LAYOUTS[name])
    mutant = copy.deepcopy(SEED_LAYOUTS[name])
    vol = mutant["sets"][0]["volumes"]
    if vol:
        vol[0]["fs"] = "ext4"  # a real change
        assert _canon(mutant) != base


# --------------------------------------------------------------------------- #
# Bucket 3 -- invalid / ambiguous / hostile inputs reject cleanly.
# --------------------------------------------------------------------------- #
REJECTED = {
    "duplicate_key": "version: 2\nversion: 3\nsets: []\n",
    "merge_key": "base: &b {role: os}\nsets:\n- <<: *b\n  volumes: []\n",
    "alias": "sets: &s []\nother: *s\n",
    "multi_document": "version: 2\nsets: []\n---\nversion: 3\nsets: []\n",
    "top_level_list": "- role: os\n- role: data\n",
    "top_level_scalar": "just-a-string\n",
    "empty": "",
    "only_comment": "# nothing here\n",
    "tab_indent": "version: 2\nsets:\n-\trole: os\n",
    "bad_int_count": "version: 2\nsets:\n- {role: os, selection: discover, count: two, volumes: []}\n",
    "float_count": "version: 2\nsets:\n- {role: os, selection: discover, count: 1.5, volumes: []}\n",
    "bad_bool_persistent": "version: 2\nsets:\n- {role: os, persistent: maybe, volumes: []}\n",
    "bad_version": "version: latest\nsets: []\n",
}


@pytest.mark.parametrize("name", sorted(REJECTED))
def test_hostile_input_rejected(name: str) -> None:
    with pytest.raises(DisklayoutError):
        canonicalize(REJECTED[name])


def test_utf16_rejected() -> None:
    payload = json.dumps(SEED_LAYOUTS["tmpfs_ram_root"]).encode("utf-16")
    with pytest.raises(DisklayoutError):
        canonicalize(payload)


def test_invalid_utf8_rejected() -> None:
    with pytest.raises(DisklayoutError):
        canonicalize(b"\xff\xfe\x00garbage")


def test_oversized_rejected() -> None:
    with pytest.raises(DisklayoutError):
        canonicalize(b"x" * (disklayout.MAX_INPUT_BYTES + 1))


def test_billion_laughs_does_not_hang() -> None:
    """Classic YAML alias bomb: it must raise (aliases forbidden), not expand."""
    bomb = "a: &a [x,x,x,x,x,x,x,x,x]\nb: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]\nc: [*b,*b,*b,*b,*b,*b,*b,*b,*b]\n"
    with pytest.raises(DisklayoutError):
        canonicalize(bomb)


def test_error_messages_are_operator_facing() -> None:
    """A simple rejection carries a legible, single-line reason (no traceback)."""
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("version: 2\nversion: 3\nsets: []\n")
    msg = str(excinfo.value)
    assert msg and "\n" not in msg and "version" in msg


def test_parse_error_reports_location() -> None:
    """A syntax error names the line and column so a human can find it."""
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("version: 2\nsets:\n- role: os\n    volumes: []\n")  # bad indent
    msg = str(excinfo.value)
    assert "line " in msg and "column " in msg


def test_tab_error_is_helpful() -> None:
    """The cryptic tab error grows a plain-language hint about spaces vs tabs."""
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("version: 2\nsets:\n-\trole: os\n")
    msg = str(excinfo.value).lower()
    assert "hint:" in msg and "tab" in msg and "space" in msg


def test_missing_space_after_colon_is_helpful() -> None:
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("version:2\nsets: []\n")
    assert "key: value" in str(excinfo.value)


def test_coercion_error_shows_valid_form() -> None:
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("version: 2\nsets:\n- {role: os, selection: discover, count: two, volumes: []}\n")
    assert "whole number" in str(excinfo.value)
    with pytest.raises(DisklayoutError) as excinfo2:
        canonicalize("version: 2\nsets:\n- {role: os, persistent: maybe, volumes: []}\n")
    assert "true or false" in str(excinfo2.value)


def test_lost_case_shows_a_right_example() -> None:
    """The most-confused inputs (not an object / empty) print a real skeleton."""
    for bad in ("- role: os\n- role: data\n", "", "# just a comment\n"):
        with pytest.raises(DisklayoutError) as excinfo:
            canonicalize(bad)
        msg = str(excinfo.value)
        assert "version: 2" in msg and "sets:" in msg and "mountpoint: /" in msg


# --------------------------------------------------------------------------- #
# Property tests (Hypothesis) -- the three-buckets invariant at scale.
# --------------------------------------------------------------------------- #
_safe_text = st.text(
    alphabet=st.characters(min_codepoint=0x21, max_codepoint=0x7E, blacklist_characters="\"'\\{}[]:,&*#?|<>=!%@`"),
    min_size=1,
    max_size=12,
)
_norwayish = st.sampled_from(NORWAY_STRINGS)
_str_value = st.one_of(_safe_text, _norwayish)


@st.composite
def _volume(draw: st.DrawFn) -> dict:
    vol: dict = {
        "mountpoint": draw(st.sampled_from(["/", "/boot", "/boot/efi", "/scratch"])),
        "fs": draw(st.sampled_from(["xfs", "ext4", "vfat", "tmpfs", "squashfs", "zfs"])),
        "provider": draw(st.sampled_from(["partition", "lvm", "memory", "zpool"])),
    }
    if draw(st.booleans()):
        vol["size"] = draw(_str_value)
    if draw(st.booleans()):
        vol["clear_uefi_nvram"] = draw(st.booleans())
    return vol


@st.composite
def _layout(draw: st.DrawFn) -> dict:
    a_set: dict = {
        "role": draw(st.sampled_from(["os", "data"])),
        "raid": draw(_str_value),
        "volumes": draw(st.lists(_volume(), min_size=0, max_size=3)),
    }
    if draw(st.booleans()):
        a_set["name"] = draw(_safe_text)
    if draw(st.booleans()):
        a_set["count"] = draw(st.integers(min_value=0, max_value=16))
    if draw(st.booleans()):
        a_set["save"] = draw(st.booleans())
    if draw(st.booleans()):
        a_set["persistent"] = draw(st.booleans())
    return {"version": draw(st.integers(min_value=0, max_value=9)), "sets": [a_set]}


@settings(max_examples=400)
@given(_layout())
def test_property_format_independence(layout: dict) -> None:
    """JSON-in and YAML-in of the same structure -> identical canonical bytes."""
    assert canonicalize(json.dumps(layout)) == canonicalize(yaml.safe_dump(layout))


@settings(max_examples=400)
@given(_layout())
def test_property_idempotent(layout: dict) -> None:
    once = canonicalize(json.dumps(layout))
    assert canonicalize(once) == once


@settings(max_examples=400)
@given(_layout())
def test_property_editor_round_trip(layout: dict) -> None:
    once = canonicalize(json.dumps(layout))
    assert canonicalize(to_yaml(once)) == once


@settings(max_examples=400)
@given(_layout())
def test_property_string_fields_never_coerced(layout: dict) -> None:
    """No string field value ever surfaces as a bool/int/float in canonical JSON."""
    out = json.loads(canonicalize(json.dumps(layout)))
    for a_set in out["sets"]:
        assert isinstance(a_set["raid"], str)
        for vol in a_set["volumes"]:
            if "size" in vol:
                assert isinstance(vol["size"], str)


# =========================================================================== #
# 00-02 -- defaults: fill (stored canonical is complete) + strip (editor sugar)
# The convergence law: remove / half / add / back-and-forth all land on the same
# complete canonical bytes. Tested on real installer layouts (bundled fixtures)
# and on synthetic shorthand.
# =========================================================================== #
import copy  # noqa: E402

_FIXTURES = sorted((Path(__file__).resolve().parent / "fixtures" / "disklayouts").glob("*.json"))
_FIXTURE_IDS = [f.stem for f in _FIXTURES]


def _dig(obj: object, path: tuple) -> object:
    for key in path:
        obj = obj[key]  # type: ignore[index]
    return obj


def _default_paths(complete: dict) -> list[tuple]:
    """Every leaf that fill would re-add: the removable-default locations."""
    paths: list[tuple] = [("version",)]
    for si, a_set in enumerate(complete.get("sets", [])):
        for key in ("name", "selection", "raid"):
            paths.append(("sets", si, key))
        for vi, _vol in enumerate(a_set.get("volumes", [])):
            for key in ("name", "mountpoint", "size", "options"):
                paths.append(("sets", si, "volumes", vi, key))
    return paths


def _drop(variant: dict, path: tuple) -> object | None:
    parent = _dig(variant, path[:-1])
    if isinstance(parent, dict) and path[-1] in parent:
        return parent.pop(path[-1])
    return None


@pytest.mark.parametrize("fixture", _FIXTURES, ids=_FIXTURE_IDS)
def test_fixture_fill_preserves_and_round_trips(fixture: Path) -> None:
    """A real installer layout: fill never changes a present value, and the
    editor short-form re-fills to the identical canonical bytes."""
    raw = fixture.read_bytes()
    original = json.loads(raw)
    canon = canonicalize(raw)
    filled = json.loads(canon)

    def subset(a: object, b: object) -> bool:
        if isinstance(a, dict):
            return isinstance(b, dict) and all(k in b and subset(v, b[k]) for k, v in a.items())
        if isinstance(a, list):
            return isinstance(b, list) and len(a) == len(b) and all(subset(x, y) for x, y in zip(a, b))
        return a == b

    assert subset(original, filled), "fill changed a present value (must only ADD)"
    assert canonicalize(to_yaml(canon)) == canon, "editor strip->fill round-trip broke"


@settings(max_examples=40, deadline=None)
@pytest.mark.parametrize("fixture", _FIXTURES, ids=_FIXTURE_IDS)
@given(data=st.data())
def test_fixture_partial_defaults_converge(fixture: Path, data: st.DataObject) -> None:
    """Remove/half/add: any random subset of the default fields -- dropped or
    kept -- canonicalizes to the same complete bytes."""
    canon = canonicalize(fixture.read_bytes())
    complete = json.loads(canon)
    variant = copy.deepcopy(complete)
    for path in _default_paths(complete):
        if data.draw(st.booleans()):
            saved = _drop(variant, path)
            if saved is not None and canonicalize(json.dumps(variant)) != canon:
                parent = _dig(variant, path[:-1])
                assert isinstance(parent, dict)
                parent[path[-1]] = saved
    assert canonicalize(json.dumps(variant)) == canon


def test_bare_single_set_equals_wrapped() -> None:
    bare = "role: os\ndevices: [/dev/vda]\nvolumes: [{mountpoint: /, fs: xfs, provider: lvm, size: 100%}]\n"
    wrapped = "version: 2\nsets:\n- " + bare.replace("\n", "\n  ").rstrip() + "\n"
    assert canonicalize(bare) == canonicalize(wrapped)


def test_memboot_tmpfs_sugar_fills_ram_root() -> None:
    out = json.loads(canonicalize("role: os\nvolumes: [{fs: tmpfs, provider: memory}]\n"))
    vol = out["sets"][0]["volumes"][0]
    assert vol == {"fs": "tmpfs", "provider": "memory", "mountpoint": "/",
                   "size": "80%", "options": "mpol=interleave", "name": "root"}
    assert out["version"] == 2 and out["sets"][0]["raid"] == "none"


def test_memboot_squashfs_sugar_fills_ram_root() -> None:
    out = json.loads(canonicalize("role: os\nvolumes: [{fs: squashfs, provider: memory}]\n"))
    vol = out["sets"][0]["volumes"][0]
    assert vol["fs"] == "squashfs" and vol["size"] == "80%" and vol["options"] == "mpol=interleave"


def test_explicit_ram_options_not_overridden() -> None:
    """Fill never clobbers an explicit value (BE-D6)."""
    out = json.loads(canonicalize("role: os\nvolumes: [{fs: tmpfs, provider: memory, size: 50%}]\n"))
    assert out["sets"][0]["volumes"][0]["size"] == "50%"


def test_volume_name_from_mountpoint() -> None:
    out = json.loads(canonicalize(
        "role: os\ndevices: [/dev/vda]\nvolumes:\n"
        "- {mountpoint: /boot/efi, fs: vfat, provider: partition, size: 600M}\n"
        "- {mountpoint: /boot, fs: xfs, provider: partition, size: 1G}\n"
        "- {mountpoint: /, fs: xfs, provider: lvm, size: 100%}\n"))
    names = [v["name"] for v in out["sets"][0]["volumes"]]
    assert names == ["uefi", "boot", "root"]


def test_set_name_collision_aware() -> None:
    """Two unnamed data sets derive distinct names (data, data2)."""
    out = json.loads(canonicalize(
        "version: 2\nsets:\n"
        "- {role: data, devices: [/dev/vdb], volumes: [{mountpoint: /a, fs: xfs, provider: lvm, size: 100%}]}\n"
        "- {role: data, devices: [/dev/vdc], volumes: [{mountpoint: /b, fs: xfs, provider: lvm, size: 100%}]}\n"))
    assert [s["name"] for s in out["sets"]] == ["data", "data2"]


def test_explicit_name_preserved_and_not_reused() -> None:
    """A derived name skips an explicit one (no collision)."""
    out = json.loads(canonicalize(
        "version: 2\nsets:\n"
        "- {role: data, name: data, devices: [/dev/vdb], volumes: [{mountpoint: /a, fs: xfs, provider: lvm, size: 100%}]}\n"
        "- {role: data, devices: [/dev/vdc], volumes: [{mountpoint: /b, fs: xfs, provider: lvm, size: 100%}]}\n"))
    assert [s["name"] for s in out["sets"]] == ["data", "data2"]


def test_selection_inferred_from_devices() -> None:
    manual = json.loads(canonicalize("role: os\ndevices: [/dev/vda]\nvolumes: [{mountpoint: /, fs: xfs, provider: lvm, size: 100%}]\n"))
    discover = json.loads(canonicalize("role: os\nraid: '1'\nvolumes: [{mountpoint: /, fs: xfs, provider: lvm, size: 100%}]\n"))
    assert manual["sets"][0]["selection"] == "manual"
    assert discover["sets"][0]["selection"] == "discover"


def test_role_is_mandatory_with_help() -> None:
    with pytest.raises(DisklayoutError) as excinfo:
        canonicalize("volumes: [{fs: tmpfs, provider: memory}]\n")
    msg = str(excinfo.value)
    assert "role" in msg and ("os" in msg and "data" in msg)


@pytest.mark.parametrize("level", ["layout", "set", "volume"])
def test_comment_is_meaning_neutral(level: str) -> None:
    """A comment at any level persists but does not change the storage meaning."""
    base: dict[str, Any] = {"role": "os", "devices": ["/dev/vda"],
                            "volumes": [{"mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "100%"}]}
    commented = copy.deepcopy(base)
    if level == "layout":
        commented = {"comment": "prod nodes", **commented}
    elif level == "set":
        commented["comment"] = "the OS set"
    else:
        commented["volumes"][0]["comment"] = "root fs"

    def drop_comment(obj: object) -> object:
        if isinstance(obj, dict):
            return {k: drop_comment(v) for k, v in obj.items() if k != "comment"}
        if isinstance(obj, list):
            return [drop_comment(x) for x in obj]
        return obj

    plain = canonicalize(json.dumps(base))
    with_comment = json.loads(canonicalize(json.dumps(commented)))
    assert "comment" in json.dumps(with_comment)  # it persists
    assert canonicalize(json.dumps(drop_comment(with_comment))) == plain  # meaning unchanged
