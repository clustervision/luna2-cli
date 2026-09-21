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
Test battery for Helper().brief_disklayout -- the one-glance disklayout block
that `luna node|group show` prints in its table.

Two properties, and the second is the one that will get broken by accident:

  (1) a stored layout renders as a set header plus its volumes, and anything
      unusable degrades to a marker instead of taking `show` down with it;
  (2) the rendering stays inside three newlines per set. `show` pipes the value
      through Helper().less_content, which keeps only the FIRST THREE LINES of
      any content longer than 60 characters. A line-per-volume rendering reads
      better in isolation and silently loses most of itself on screen, so the
      packed form is a requirement rather than a style choice.

luna.utils.log refuses to initialise without root -- logging.basicConfig cannot
open LOG_FILE -- so the logger is stubbed rather than initialised. That is the
only privilege the module wants; importing and using Helper needs nothing else.
"""
from __future__ import annotations

import json
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    """Give Helper a logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


@pytest.fixture
def helper():
    from luna.utils.helper import Helper
    return Helper()


LAYOUT = json.dumps({
    "version": 2,
    "sets": [{
        "name": "os", "role": "os", "selection": "discover", "raid": "none",
        "volumes": [
            {"name": "uefi", "mountpoint": "/boot/efi", "fs": "vfat", "provider": "partition", "size": "600M"},
            {"name": "boot", "mountpoint": "/boot", "fs": "xfs", "provider": "partition", "size": "1G"},
            {"name": "swap", "mountpoint": "swap", "fs": "swap", "provider": "lvm", "size": "2G"},
            {"name": "root", "mountpoint": "/", "fs": "xfs", "provider": "lvm", "size": "20G"},
            {"name": "var", "mountpoint": "/var", "fs": "ext4", "provider": "lvm", "size": "100%"},
        ],
    }],
})

MARKER = '<unreadable disklayout JSON - see showdisklayout -R>'


def test_renders_set_header_and_one_volume_line(helper) -> None:
    assert helper.brief_disklayout(LAYOUT) == (
        "set = os (discover, raid none)\n"
        "  /boot/efi vfat 600M, /boot xfs 1G, swap 2G, / xfs 20G, /var ext4 100%"
    )


def test_survives_the_show_length_limiter(helper) -> None:
    """
    The regression that matters. less_content keeps three lines; prove the
    rendering fits, and prove it by running the real limiter over it rather
    than by counting newlines and hoping the limit never moves.
    """
    rendered = helper.brief_disklayout(LAYOUT)
    assert helper.less_content(rendered, True) == rendered


def test_does_not_repeat_swap_twice(helper) -> None:
    rendered = helper.brief_disklayout(LAYOUT)
    assert "swap 2G" in rendered
    assert "swap swap" not in rendered


def test_names_manual_devices_instead_of_the_selector(helper) -> None:
    doc = json.loads(LAYOUT)
    doc["sets"][0]["selection"] = "manual"
    doc["sets"][0]["devices"] = ["/dev/sda", "/dev/sdb"]
    assert helper.brief_disklayout(json.dumps(doc)).startswith(
        "set = os (/dev/sda, /dev/sdb, raid none)")


def test_renders_every_set(helper) -> None:
    doc = json.loads(LAYOUT)
    doc["sets"].append({"name": "data", "role": "data", "selection": "manual",
                        "devices": ["/dev/sdc"], "raid": "1",
                        "volumes": [{"name": "d", "mountpoint": "/data",
                                     "fs": "xfs", "provider": "lvm", "size": "100%"}]})
    rendered = helper.brief_disklayout(json.dumps(doc))
    assert "set = os (" in rendered
    assert "set = data (/dev/sdc, raid 1)" in rendered


@pytest.mark.parametrize("empty", ["", "   ", "\n", None])
def test_no_layout_is_passed_through_untouched(helper, empty) -> None:
    """
    No layout declared is legal -- install_mode=auto falls back to a RAM root --
    so the value is handed back for `show` to render as <empty>, not replaced
    with an error marker.
    """
    assert helper.brief_disklayout(empty) == empty


@pytest.mark.parametrize("bad", [
    "{not json",
    "[]",
    '{"sets": "not-a-list"}',
    '{"sets": ["not-an-object"]}',
    '{"sets": [{"name": "os", "volumes": ["not-an-object"]}]}',
])
def test_unusable_layouts_degrade_instead_of_raising(helper, bad: str) -> None:
    """`show` must survive whatever is stored; a bad layout costs one field."""
    assert helper.brief_disklayout(bad) == MARKER


def test_tolerates_a_set_with_no_volumes(helper) -> None:
    assert helper.brief_disklayout(json.dumps({
        "version": 2,
        "sets": [{"name": "os", "raid": "none", "selection": "discover"}],
    })) == "set = os (discover, raid none)"
