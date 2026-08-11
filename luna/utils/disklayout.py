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
YAML/JSON front-end for the node ``disklayout`` attribute.

The node-side installer consumes the storage layout as a JSON document. Hand
authoring JSON is noisy, so the CLI accepts the layout as YAML *or* JSON on both
the ``-q<key> <file>`` load path and the ``$EDITOR`` path, and canonicalizes it
to JSON before it is stored. YAML is a JSON superset, so every existing JSON
layout remains valid input and nothing downstream changes: the daemon still
stores, and the node still receives, a JSON string.

The one hazard this module exists to close is YAML's implicit scalar typing (the
"Norway problem": ``no`` -> False, ``10`` -> int, ``0600`` -> octal, ``1:30`` ->
sexagesimal, ``1e3`` -> float). The disklayout schema is almost entirely
strings; a silently coerced scalar would change a layout's meaning without the
operator ever seeing it. PyYAML has no typed-struct unmarshal (unlike Go's
yaml.v3), so we cannot lean on the parser to do the right thing. Instead we parse
with a string-preserving loader -- every plain scalar stays a ``str`` -- and then
EXPLICITLY coerce the handful of fields the schema defines as int/bool, failing
loud on anything that will not coerce. No parser magic, no silent fallback.

The schema field types mirror ``internal/config/v2/types.go`` in luna2-client:

    ints  : version, count, spares
    bools : save, persistent, clear_uefi_nvram
    everything else is a string (or a list/map of strings).

This module is a pure front-end (contract C2): its only output is canonical JSON
bytes or a clean ``DisklayoutError``. It does not validate storage semantics --
role/topology/device checks stay in the node-side v2 validator, which sees the
canonical JSON unchanged.
"""
from __future__ import annotations

import codecs
import json
import re
from typing import Any

import yaml

__author__ = "ClusterVision Solutions b.v."
__copyright__ = "Copyright 2025, Luna2 Project [CLI]"
__license__ = "GPL"

# Guard against pathological input before the parser ever sees it (the YAML
# "billion laughs" alias-expansion vector is separately blocked below, but a
# hard byte ceiling is a cheap belt for any large-payload attempt).
MAX_INPUT_BYTES = 1 << 20  # 1 MiB -- a disklayout is a few hundred bytes.

# The only supported schema version (mirrors v2 SchemaVersion in types.go). Filled
# when absent; the node-side validator requires version == this value.
SchemaVersion = 2

# Fields the v2 schema defines as non-string. Everything not listed here stays a
# string after parse. Key names are globally unambiguous (no string field is
# named "count"/"save"/...), so a recursive key-based coercion is safe.
_INT_FIELDS = frozenset({"version", "count", "spares"})
_BOOL_FIELDS = frozenset({"save", "persistent", "clear_uefi_nvram"})

# YAML-1.1 boolean words we accept in the declared bool fields (case-folded).
# These are exactly the words PyYAML would otherwise coerce implicitly; we accept
# them ONLY here and keep them as literal strings everywhere else.
_TRUE_WORDS = frozenset({"true", "yes", "on", "y"})
_FALSE_WORDS = frozenset({"false", "no", "off", "n"})


class DisklayoutError(ValueError):
    """A disklayout document could not be canonicalized. Message is operator-facing."""


class _StrLoader(yaml.SafeLoader):
    """A SafeLoader that keeps every plain scalar a string and refuses YAML sugar.

    Typed scalar tags (bool/int/float/timestamp) are neutralized to ``str`` so
    the Norway problem cannot bite; explicit ``null`` is preserved as ``None``
    (faithful JSON). Duplicate mapping keys, merge keys, and aliases are hard
    errors -- a disklayout is a flat data document, none of them can appear
    without an authoring mistake or a hostile payload.
    """

    def compose_node(self, parent: Any, index: Any) -> Any:
        # Refuse aliases (and thus the "billion laughs" expansion DoS). Anchors
        # without a referencing alias are inert, but an alias event only exists
        # to expand one, so blocking it here closes the vector.
        if self.check_event(yaml.events.AliasEvent):  # type: ignore[no-untyped-call]
            raise DisklayoutError("YAML anchors and aliases aren't supported")
        return super().compose_node(parent, index)


def _construct_str(loader: yaml.SafeLoader, node: yaml.nodes.Node) -> str:
    return str(loader.construct_scalar(node))  # type: ignore[arg-type]


def _construct_mapping_nodup(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> dict[str, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        if key_node.tag == "tag:yaml.org,2002:merge":
            raise DisklayoutError("YAML merge keys (<<) aren't supported")
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise DisklayoutError(f"keys must be text, got {type(key).__name__}")
        if key in mapping:
            raise DisklayoutError(f"duplicate key '{key}'")
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


for _tag in (
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
    "tag:yaml.org,2002:timestamp",
):
    _StrLoader.add_constructor(_tag, _construct_str)
_StrLoader.add_constructor("tag:yaml.org,2002:map", _construct_mapping_nodup)


def _decode(raw: bytes | str) -> str:
    """Decode input bytes to a UTF-8 string, tolerating a UTF-8 BOM only."""
    if isinstance(raw, str):
        return raw
    if len(raw) > MAX_INPUT_BYTES:
        raise DisklayoutError("disklayout is too big")
    for bom in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        if raw.startswith(bom):
            raise DisklayoutError("disklayout must be UTF-8")
    try:
        return raw.decode("utf-8-sig")  # strips a leading UTF-8 BOM if present
    except UnicodeDecodeError as err:
        raise DisklayoutError("not valid UTF-8") from err


def _coerce_int(key: str, value: Any) -> int:
    if isinstance(value, bool):
        raise DisklayoutError(f"{key} must be a whole number, not true/false")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip(), 10)
        except ValueError:
            raise DisklayoutError(f"{key} must be a whole number, got '{value}'") from None
    raise DisklayoutError(f"{key} must be a whole number, got {type(value).__name__}")


def _coerce_bool(key: str, value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        folded = value.strip().lower()
        if folded in _TRUE_WORDS:
            return True
        if folded in _FALSE_WORDS:
            return False
    raise DisklayoutError(f"{key} must be true or false, got '{value}'")


def _coerce(node: Any) -> Any:
    """Recursively apply the explicit typed coercion to the parsed structure."""
    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in _INT_FIELDS:
                out[key] = _coerce_int(key, value)
            elif key in _BOOL_FIELDS:
                out[key] = _coerce_bool(key, value)
            else:
                out[key] = _coerce(value)
        return out
    if isinstance(node, list):
        return [_coerce(item) for item in node]
    return node


# A right-example for the most-lost case (top-level not an object / empty). Kept
# to a single, real, minimal layout -- enough to unstick a human without a wall
# of docs.
_SKELETON = (
    "example:\n"
    "  version: 2\n"
    "  sets:\n"
    "    - role: os\n"
    "      devices: [/dev/vda]\n"
    "      volumes: [/boot/efi, /boot, /]"
)

# Short, plain hints for PyYAML's most cryptic complaints, matched as substrings
# against the parser's `problem` text.
_YAML_HINTS = (
    ("mapping values are not allowed here",
     "missing space after ':' (write 'key: value'), or wrong indentation"),
    ("cannot start any token",
     "invalid character, often a tab. use spaces, not tabs"),
    ("could not find expected ':'",
     "missing ':' or inconsistent indentation"),
    ("while scanning a quoted scalar",
     "unclosed quote"),
    ("while parsing a flow",
     "unclosed '[' or '{', or a stray ',' or ':'"),
    ("while parsing a block",
     "check indentation: items under a key must line up"),
)


def _yaml_hint(problem: str) -> str:
    for needle, advice in _YAML_HINTS:
        if needle in problem:
            return advice
    return ""


def _parse(text: str) -> Any:
    try:
        return yaml.load(text, Loader=_StrLoader)  # noqa: S506 -- _StrLoader is a SafeLoader subclass
    except DisklayoutError:
        raise
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None) or getattr(err, "context_mark", None)
        where = f" at line {mark.line + 1}, column {mark.column + 1}" if mark is not None else ""
        problem = getattr(err, "problem", None) or str(err).splitlines()[0]
        hint = _yaml_hint(problem)
        raise DisklayoutError(f"invalid YAML{where}: {hint or problem}") from err


# --------------------------------------------------------------------------- #
# Defaults. The stored canonical form is COMPLETE (every default materialized),
# so a human's shorthand and its fully-spelled twin canonicalize to identical
# bytes, and the node-side v2 validator -- which has NO defaulting of its own and
# *requires* role/name/selection/raid/version/sets -- receives a layout it will
# accept without re-deriving anything (no CLI<->validator drift). Authoring is
# terse (bare-string / token-list / map volume shorthand + conventions, BE-V);
# the editor ECHOES the full resolved form (to_yaml, BE-R echo-full), not a
# stripped minimum -- terse IN, explicit OUT.
#
# What is filled (absent only, never overriding a set value) and the v2 rule it
# satisfies (internal/config/v2/validate.go):
#   version  <- 2                        (must == SchemaVersion)
#   sets[]   <- wrap a bare single set   (top-level requires a non-empty sets[])
#   set.name       <- role + ordinal     (name is required; collision-aware)
#   set.selection  <- manual iff devices else discover   (selection is required)
#   set.raid       <- none               (raid is required)
#   volume.name    <- from mountpoint    (name is required)
#   memory volume  <- mountpoint '/', size 80%, options mpol=interleave (safety)
# role stays MANDATORY (it cannot be guessed); count/spares/save/persistent are
# left as authored (count 0 = "resolve per raid mode" on the node).

_MOUNT_VOLUME_NAMES = {"/": "root", "/boot": "boot", "/boot/efi": "uefi"}


def _unique(base: str, taken: set[str]) -> str:
    name = base
    n = 2
    while name in taken:
        name = f"{base}{n}"
        n += 1
    return name


def _derive_volume_name(mountpoint: str, taken: set[str]) -> str:
    base = _MOUNT_VOLUME_NAMES.get(mountpoint)
    if base is None:
        base = re.sub(r"[^a-z0-9]+", "-", mountpoint.strip("/").lower()).strip("-") or "vol"
    return _unique(base, taken)


# Volume authoring shorthand (BE-V). A volume may be a bare mountpoint STRING, a
# token LIST (shape-classified, order-free), or the explicit MAP -- all three fill
# to the same full canonical map. Mountpoint conventions supply fs/provider/size
# when absent; a supplied value always wins (fill-absent-only).
_MOUNT_CONV: dict[str, tuple[str, str, str | None]] = {
    "/boot/efi": ("vfat", "partition", "600M"),
    "/boot": ("xfs", "partition", "1G"),
    "/": ("xfs", "lvm", "100%"),
    "swap": ("swap", "partition", None),  # size must be supplied
}
# Any other (data) mount: xfs on lvm, size REQUIRED (None -> not defaulted).
_DEFAULT_CONV: tuple[str, str, str | None] = ("xfs", "lvm", None)

_FS_VALUES = frozenset({"vfat", "xfs", "ext4", "swap"})
_PROVIDER_VALUES = frozenset({"partition", "lvm", "memory", "zpool"})
_SIZE_RE = re.compile(r"^\d+(\.\d+)?%$|^\d+(\.\d+)?[KMGTP]?$")


def _classify_token(token: str) -> tuple[str, str]:
    """Classify one shorthand token by SHAPE (order-free). A '/' path or the
    literal 'swap' is the mountpoint; the rest are fs / provider / size by their
    disjoint value spaces. An unrecognized token FAILS LOUD -- never silently
    dropped nor coerced to a mountpoint (BE-V1)."""
    tok = token.strip()
    if tok.startswith("/") or tok == "swap":
        return "mountpoint", tok
    if tok in _FS_VALUES:
        return "fs", tok
    if tok in _PROVIDER_VALUES:
        return "provider", tok
    if _SIZE_RE.match(tok):
        return "size", tok
    raise DisklayoutError(
        f"bad volume token '{token}': want a /mountpoint, a size (50G, 100%), an fs, or a provider"
    )


def _parse_volume(vol: Any) -> dict[str, Any]:
    """Type-dispatch a volume to a dict (BE-V6): a bare string is a mountpoint; a
    list is shape-classified tokens (order-free); a map passes through."""
    if isinstance(vol, dict):
        return vol
    if isinstance(vol, str):
        return {"mountpoint": vol}
    if isinstance(vol, list):
        out: dict[str, Any] = {}
        for token in vol:
            if not isinstance(token, str):
                raise DisklayoutError(f"volume token must be text, got {type(token).__name__}")
            cls, value = _classify_token(token)
            if cls in out:  # BE-V2: two of the same class
                raise DisklayoutError(f"volume has two {cls}: '{out[cls]}' and '{value}'")
            out[cls] = value
        if "mountpoint" not in out:  # BE-V3: identity cannot be defaulted
            raise DisklayoutError(f"volume has no mountpoint: {vol}")
        return out
    raise DisklayoutError(f"volume must be a string, list, or map, got {type(vol).__name__}")


def _fill_volume(vol: dict[str, Any], taken: set[str]) -> dict[str, Any]:
    vol = dict(vol)
    if vol.get("provider") == "memory":  # RAM-root safety defaults
        vol.setdefault("mountpoint", "/")
        vol.setdefault("size", "80%")
        vol.setdefault("options", "mpol=interleave")
    else:  # disk volume: mountpoint-convention defaults (BE-V4), fill-absent-only
        mountpoint = vol.get("mountpoint")
        if isinstance(mountpoint, str):
            conv_fs, conv_provider, conv_size = _MOUNT_CONV.get(mountpoint, _DEFAULT_CONV)
            vol.setdefault("fs", conv_fs)
            vol.setdefault("provider", conv_provider)
            if conv_size is not None:
                vol.setdefault("size", conv_size)
    if "name" not in vol:
        mountpoint = vol.get("mountpoint")
        if isinstance(mountpoint, str):
            vol["name"] = _derive_volume_name(mountpoint, taken)
    name = vol.get("name")
    if isinstance(name, str):
        taken.add(name)
    return vol


def _fill_set(a_set: dict[str, Any]) -> dict[str, Any]:
    if "role" not in a_set:
        raise DisklayoutError("set needs 'role: os' or 'role: data'\n" + _SKELETON)
    a_set = dict(a_set)
    a_set.setdefault("selection", "manual" if a_set.get("devices") else "discover")
    a_set.setdefault("raid", "none")
    volumes = a_set.get("volumes")
    if isinstance(volumes, list):
        parsed = [_parse_volume(v) for v in volumes]  # string/list/map -> dict (BE-V)
        taken: set[str] = set()
        for vol in parsed:
            name = vol.get("name")
            if isinstance(name, str):
                taken.add(name)
        a_set["volumes"] = [_fill_volume(v, taken) for v in parsed]
    return a_set


def _fill_defaults(doc: dict[str, Any]) -> dict[str, Any]:
    if "sets" not in doc and ("role" in doc or "volumes" in doc):
        doc = {"sets": [doc]}  # a bare single set -> wrap it
    else:
        doc = dict(doc)
    doc.setdefault("version", SchemaVersion)
    sets = doc.get("sets")
    if isinstance(sets, list):
        filled = [_fill_set(s) if isinstance(s, dict) else s for s in sets]
        taken_names: set[str] = set()
        for a_set in filled:
            if isinstance(a_set, dict):
                name = a_set.get("name")
                if isinstance(name, str):
                    taken_names.add(name)
        for a_set in filled:
            if isinstance(a_set, dict) and "name" not in a_set:
                role = a_set.get("role")
                if isinstance(role, str):
                    a_set["name"] = _unique(role, taken_names)
                    taken_names.add(a_set["name"])
        doc["sets"] = filled
    return doc


def canonicalize(raw: bytes | str) -> bytes:
    """Canonicalize a YAML-or-JSON disklayout document to canonical JSON bytes.

    Returns compact, key-sorted UTF-8 JSON with defaults filled (the complete
    stored form). Raises :class:`DisklayoutError` with an operator-facing message
    on any malformed, ambiguous, or hostile input.
    """
    parsed = _parse(_decode(raw))
    if parsed is None:
        raise DisklayoutError(f"disklayout is empty\n{_SKELETON}")
    if not isinstance(parsed, dict):
        raise DisklayoutError(f"disklayout must be an object, got a {type(parsed).__name__}\n{_SKELETON}")
    filled = _fill_defaults(_coerce(parsed))
    return json.dumps(filled, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def to_yaml(raw: bytes | str) -> str:
    """Render a stored (canonical JSON) disklayout as YAML for the editor.

    ECHO-FULL (operator 2026-07-21): the editor shows the FULL resolved layout --
    every default materialized -- so a human sees exactly what the shorthand
    became and never edits blind. It is NOT stripped to a minimum; re-parsing the
    echoed YAML canonicalizes back to identical bytes.
    """
    try:
        obj = json.loads(_decode(raw))
    except json.JSONDecodeError as err:
        raise DisklayoutError(f"stored layout is not valid JSON: {err}") from err
    # default_flow_style=None renders leaf collections (each volume map, the
    # devices list) inline on one line for readability while the structure stays
    # block. No sort_keys kwarg -> works across PyYAML 3.x-6.x (CLI runs 3.10/6.0.2).
    return yaml.safe_dump(obj, default_flow_style=None, allow_unicode=True)
