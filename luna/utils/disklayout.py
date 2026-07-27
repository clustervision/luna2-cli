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
from typing import Any

import yaml

__author__ = "ClusterVision Solutions b.v."
__copyright__ = "Copyright 2025, Luna2 Project [CLI]"
__license__ = "GPL"

# Guard against pathological input before the parser ever sees it (the YAML
# "billion laughs" alias-expansion vector is separately blocked below, but a
# hard byte ceiling is a cheap belt for any large-payload attempt).
MAX_INPUT_BYTES = 1 << 20  # 1 MiB -- a disklayout is a few hundred bytes.

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
            raise DisklayoutError("YAML aliases/anchors are not permitted in a disklayout")
        return super().compose_node(parent, index)


def _construct_str(loader: yaml.SafeLoader, node: yaml.nodes.Node) -> str:
    return str(loader.construct_scalar(node))  # type: ignore[arg-type]


def _construct_mapping_nodup(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> dict[str, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        if key_node.tag == "tag:yaml.org,2002:merge":
            raise DisklayoutError("YAML merge keys ('<<') are not permitted in a disklayout")
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise DisklayoutError(f"disklayout keys must be strings, got {type(key).__name__}")
        if key in mapping:
            raise DisklayoutError(f"duplicate key '{key}' in disklayout")
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
        raise DisklayoutError("disklayout is too large")
    for bom in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        if raw.startswith(bom):
            raise DisklayoutError("disklayout must be UTF-8 encoded (UTF-16/32 not supported)")
    try:
        return raw.decode("utf-8-sig")  # strips a leading UTF-8 BOM if present
    except UnicodeDecodeError as err:
        raise DisklayoutError("disklayout is not valid UTF-8") from err


def _coerce_int(key: str, value: Any) -> int:
    if isinstance(value, bool):
        raise DisklayoutError(f"'{key}' must be a whole number like 2, not a true/false value")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip(), 10)
        except ValueError:
            raise DisklayoutError(
                f"'{key}' must be a whole number like 2, not '{value}'"
            ) from None
    raise DisklayoutError(f"'{key}' must be a whole number like 2, not {type(value).__name__}")


def _coerce_bool(key: str, value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        folded = value.strip().lower()
        if folded in _TRUE_WORDS:
            return True
        if folded in _FALSE_WORDS:
            return False
    raise DisklayoutError(
        f"'{key}' must be true or false (yes/no are also accepted), not '{value}'"
    )


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
    "A disklayout is an object with a 'sets' list, for example:\n"
    "  version: 2\n"
    "  sets:\n"
    "    - role: os\n"
    "      devices: [/dev/vda]\n"
    "      volumes:\n"
    "        - {mountpoint: /, fs: xfs, provider: lvm, size: 100%}"
)

# Plain-language advice for PyYAML's most common (and most cryptic) complaints,
# matched as substrings against the parser's `problem` text.
_YAML_HINTS = (
    ("mapping values are not allowed here",
     "usually a missing space after a colon (write 'key: value', not 'key:value'), "
     "or a key indented to the wrong level"),
    ("cannot start any token",
     "there is an invalid character here -- most often a TAB used for indentation; "
     "YAML needs spaces, not tabs"),
    ("could not find expected ':'",
     "a mapping key is missing its ':' or a line is indented inconsistently"),
    ("while scanning a quoted scalar",
     "an opening quote ' or \" has no matching closing quote"),
    ("while parsing a flow",
     "a '[' or '{' was left unclosed, or there is a stray ',' or ':' inside it"),
    ("while parsing a block",
     "check the indentation -- items under a key must all line up at the same level"),
)


def _yaml_hint(problem: str) -> str:
    for needle, advice in _YAML_HINTS:
        if needle in problem:
            return f"\n  hint: {advice}"
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
        raise DisklayoutError(
            f"disklayout is not valid YAML{where}: {problem}{_yaml_hint(problem)}"
        ) from err


def canonicalize(raw: bytes | str) -> bytes:
    """Canonicalize a YAML-or-JSON disklayout document to canonical JSON bytes.

    Returns compact, key-sorted UTF-8 JSON. Raises :class:`DisklayoutError` with
    an operator-facing message on any malformed, ambiguous, or hostile input.
    """
    parsed = _parse(_decode(raw))
    if parsed is None:
        raise DisklayoutError(f"the disklayout is empty.\n{_SKELETON}")
    if not isinstance(parsed, dict):
        raise DisklayoutError(
            f"the disklayout must be an object with a 'sets' list, but this is "
            f"a {type(parsed).__name__}.\n{_SKELETON}"
        )
    coerced = _coerce(parsed)
    return json.dumps(coerced, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def to_yaml(raw: bytes | str) -> str:
    """Render a stored (canonical JSON) disklayout as YAML for the editor.

    The inverse presentation of :func:`canonicalize`: it takes what is stored
    (JSON) and produces human-friendly YAML to hand to ``$EDITOR``. Scalars that
    look typed (``raid: '10'``, ``model: 'no'``) are emitted quoted so that they
    round-trip back through :func:`canonicalize` as strings.
    """
    try:
        obj = json.loads(_decode(raw))
    except json.JSONDecodeError as err:
        raise DisklayoutError(f"stored disklayout is not valid JSON: {err}") from err
    # No sort_keys kwarg: the input is already key-sorted canonical JSON, so key
    # order is moot, and omitting it keeps this identical across PyYAML 3.x-6.x
    # (the luna CLI runs on its own Python 3.10 / PyYAML 6.0.2; 3.6/3.12 are a
    # portability belt). PyYAML 3.x predates the kwarg, so this stays compatible.
    return yaml.safe_dump(obj, default_flow_style=False, allow_unicode=True)
