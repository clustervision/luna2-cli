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

"""
The YAML-or-JSON reader the document front-ends share: the disk layout and the
network mounts are both authored as YAML or JSON and stored as canonical JSON.

The one hazard this module exists to close is YAML's implicit scalar typing (the
"Norway problem": ``no`` -> False, ``10`` -> int, ``0755`` -> octal, ``1:30`` ->
sexagesimal, ``1e3`` -> float). The documents are almost entirely strings, and a
silently coerced scalar changes a document's meaning without the operator ever
seeing it. PyYAML has no typed-struct unmarshal, so every plain scalar is kept a
``str`` here and each front-end EXPLICITLY coerces the handful of fields its
schema defines as int or bool, failing loud on anything that will not coerce.

Each front-end owns its error class so a caller can keep telling the two apart;
the functions here raise whichever class they are handed.
"""
from __future__ import annotations

import codecs
from typing import Any

import yaml

__author__ = "ClusterVision Solutions b.v."
__copyright__ = "Copyright 2026, Luna2 Project [CLI]"
__license__ = "GPL"

# Guard against pathological input before the parser ever sees it (the YAML
# "billion laughs" alias-expansion vector is separately blocked below, but a
# hard byte ceiling is a cheap belt for any large-payload attempt).
MAX_INPUT_BYTES = 1 << 20  # 1 MiB -- a document is a few hundred bytes.

# YAML-1.1 boolean words accepted in a declared bool field (case-folded).
# These are exactly the words PyYAML would otherwise coerce implicitly; they are
# accepted ONLY there and kept as literal strings everywhere else.
_TRUE_WORDS = frozenset({"true", "yes", "on", "y"})
_FALSE_WORDS = frozenset({"false", "no", "off", "n"})


class DocumentError(ValueError):
    """A document could not be canonicalized. Message is operator-facing."""


def make_loader(error: type[DocumentError]) -> type[yaml.SafeLoader]:
    """A SafeLoader that keeps every plain scalar a string and refuses YAML sugar.

    Typed scalar tags (bool/int/float/timestamp) are neutralized to ``str`` so
    the Norway problem cannot bite; explicit ``null`` is preserved as ``None``
    (faithful JSON). Duplicate mapping keys, merge keys, and aliases are hard
    errors -- these are flat data documents, none of them can appear without an
    authoring mistake or a hostile payload. Raises ``error`` on any of them.
    """

    class _StrLoader(yaml.SafeLoader):

        def compose_node(self, parent: Any, index: Any) -> Any:
            # Refuse aliases (and thus the "billion laughs" expansion DoS). Anchors
            # without a referencing alias are inert, but an alias event only exists
            # to expand one, so blocking it here closes the vector.
            if self.check_event(yaml.events.AliasEvent):  # type: ignore[no-untyped-call]
                raise error("YAML anchors and aliases aren't supported")
            return super().compose_node(parent, index)

    def _construct_str(loader: yaml.SafeLoader, node: yaml.nodes.Node) -> str:
        return str(loader.construct_scalar(node))  # type: ignore[arg-type]

    def _construct_mapping_nodup(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> dict[str, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise error("YAML merge keys (<<) aren't supported")
            key = loader.construct_object(key_node, deep=True)
            if not isinstance(key, str):
                raise error(f"keys must be text, got {type(key).__name__}")
            if key in mapping:
                raise error(f"duplicate key '{key}'")
            mapping[key] = loader.construct_object(value_node, deep=True)
        return mapping

    for tag in (
        "tag:yaml.org,2002:bool",
        "tag:yaml.org,2002:int",
        "tag:yaml.org,2002:float",
        "tag:yaml.org,2002:timestamp",
    ):
        _StrLoader.add_constructor(tag, _construct_str)
    _StrLoader.add_constructor("tag:yaml.org,2002:map", _construct_mapping_nodup)
    return _StrLoader


def decode(raw: bytes | str, label: str, error: type[DocumentError]) -> str:
    """Decode input bytes to a UTF-8 string, tolerating a UTF-8 BOM only."""
    if isinstance(raw, str):
        return raw
    if len(raw) > MAX_INPUT_BYTES:
        raise error(f"{label} is too big")
    for bom in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        if raw.startswith(bom):
            raise error(f"{label} must be UTF-8")
    try:
        return raw.decode("utf-8-sig")  # strips a leading UTF-8 BOM if present
    except UnicodeDecodeError as err:
        raise error("not valid UTF-8") from err


def coerce_int(key: str, value: Any, error: type[DocumentError]) -> int:
    if isinstance(value, bool):
        raise error(f"{key} must be a whole number, not true/false")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip(), 10)
        except ValueError:
            raise error(f"{key} must be a whole number, got '{value}'") from None
    raise error(f"{key} must be a whole number, got {type(value).__name__}")


def coerce_bool(key: str, value: Any, error: type[DocumentError]) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        folded = value.strip().lower()
        if folded in _TRUE_WORDS:
            return True
        if folded in _FALSE_WORDS:
            return False
    raise error(f"{key} must be true or false, got '{value}'")


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


def parse(text: str, loader: type[yaml.SafeLoader], error: type[DocumentError]) -> Any:
    try:
        return yaml.load(text, Loader=loader)  # noqa: S506 -- a SafeLoader subclass
    except error:
        raise
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None) or getattr(err, "context_mark", None)
        where = f" at line {mark.line + 1}, column {mark.column + 1}" if mark is not None else ""
        problem = getattr(err, "problem", None) or str(err).splitlines()[0]
        hint = _yaml_hint(problem)
        raise error(f"invalid YAML{where}: {hint or problem}") from err


def dump(obj: Any) -> str:
    """Render a parsed document as YAML for the editor: leaf collections inline
    on one line for readability while the structure stays block. No sort_keys
    kwarg -> works across PyYAML 3.x-6.x (the CLI runs on 3.10 and 6.0.2)."""
    return yaml.safe_dump(obj, default_flow_style=None, allow_unicode=True)
