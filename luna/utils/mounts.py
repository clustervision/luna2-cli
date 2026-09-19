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
YAML/JSON front-end for the ``mounts`` attribute on the cluster, a group or a node:
the network mounts document, the network twin of the disk layout.

The daemon stores and serves the document as JSON. Hand authoring JSON is noisy,
so the CLI accepts it as YAML *or* JSON on both the ``-qmnt <file>`` load path
and the ``$EDITOR`` path, and canonicalizes it to JSON before it is stored. The
parse keeps every scalar a string (see ``yamldoc``), which is the whole point
here: ``mode: 0755`` and ``mode: 1777`` are octal text for the mountpoint, and
a YAML parser left to itself would read them as numbers. The only field the
schema defines as a number is ``version``, and it is the only one coerced.

This module is a pure front-end: its only output is canonical JSON bytes or a
clean ``MountsError``. It fills nothing in beyond the version, since the design
leaves ``type`` and ``source`` defaults to the consumer, and it checks no
grammar: the daemon refuses a malformed document at store time, for every
client, with the reason.
"""
from __future__ import annotations

import json
from typing import Any

from luna.utils import yamldoc
from luna.utils.yamldoc import DocumentError

__author__ = "ClusterVision Solutions b.v."
__copyright__ = "Copyright 2026, Luna2 Project [CLI]"
__license__ = "GPL"

# The only supported schema version. Filled when absent; the daemon requires
# version == this value.
SchemaVersion = 1

_SKELETON = (
    "example:\n"
    "  mounts:\n"
    "    - path: /trinity/home\n"
    "      server: controller\n"
    "      options: nfsvers=4.2,rw,_netdev,nofail"
)


class MountsError(DocumentError):
    """A mounts document could not be canonicalized. Message is operator-facing."""


_StrLoader = yamldoc.make_loader(MountsError)


def canonicalize(raw: bytes | str) -> bytes:
    """Canonicalize a YAML-or-JSON mounts document to canonical JSON bytes.

    Returns compact, key-sorted UTF-8 JSON with the version filled. Raises
    :class:`MountsError` with an operator-facing message on any malformed,
    ambiguous, or hostile input.
    """
    parsed = yamldoc.parse(yamldoc.decode(raw, "mounts", MountsError), _StrLoader, MountsError)
    if parsed is None:
        raise MountsError(f"mounts document is empty\n{_SKELETON}")
    if not isinstance(parsed, dict):
        raise MountsError(f"mounts document must be an object, got a {type(parsed).__name__}\n{_SKELETON}")
    doc: dict[str, Any] = dict(parsed)
    doc["version"] = yamldoc.coerce_int("version", doc.get("version", SchemaVersion), MountsError)
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def to_yaml(raw: bytes | str) -> str:
    """Render a stored (canonical JSON) mounts document as YAML for the editor.
    Re-parsing the echoed YAML canonicalizes back to identical bytes."""
    try:
        obj = json.loads(yamldoc.decode(raw, "mounts", MountsError))
    except json.JSONDecodeError as err:
        raise MountsError(f"stored mounts document is not valid JSON: {err}") from err
    return yamldoc.dump(obj)
