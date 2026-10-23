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

"""A quick option takes a file path or the value in-line. Where the value can never
legitimately look like a path -- a document, or the NetworkManager ini of an interface
-- a path that does not exist used to be taken in-line: it failed as "disklayout must
be an object, got a str" and dropped the whole change, or for -qo it was stored as the
options text and reached the node. Helper.looks_like_missing_file tells the two apart,
and test_every_editor_key_is_classified keeps the next key from slipping through."""

from __future__ import annotations

import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


@pytest.fixture
def helper():
    from luna.utils.helper import Helper
    return Helper()


@pytest.mark.parametrize("key", ["disklayout", "mounts", "osimage_filter", "options", "mount"])
@pytest.mark.parametrize("value", ["/root/layut.json", "./layout.yaml", "../x.yml", "~/nope.json", "layout.json"])
def test_a_missing_path_is_reported(helper, key, value):
    assert helper.looks_like_missing_file(key, value)


@pytest.mark.parametrize("value", ['{"version": 2, "sets": []}', '[1, 2]', "version: 2\nsets: []\n", "", "   "])
def test_in_line_documents_are_not_paths(helper, value):
    assert not helper.looks_like_missing_file("disklayout", value)


def test_an_existing_file_is_not_missing(helper, tmp_path):
    f = tmp_path / "layout.json"
    f.write_text("{}")
    assert not helper.looks_like_missing_file("disklayout", str(f))


def test_other_keys_are_left_alone(helper):
    assert not helper.looks_like_missing_file("prescript", "/root/missing.sh")


# Deliberately free text: a path-like value is legitimate content for these, so a
# missing file cannot be told from the text itself. The reason per key is the
# judgement this test pins -- a new editor key fails here until it is classified.
FREE_TEXT_KEYS = {
    'content',                                  # bytes: binary secrets, profile files
    'comment',                                  # prose, may open with a path
    'prescript', 'partscript', 'postscript',    # scripts, full of paths
    'grab_filesystems',                         # mount points: '/ /boot'
    'grab_exclude',                             # path patterns
    'kerneloptions',                            # may name a device path
    'ztpconfig',                                # switch configuration text
}


def test_every_editor_key_is_classified():
    """Every editor key is either path-or-inline or deliberately free text.

    PATH_OR_INLINE_KEYS may also name a key outside the editor loop (mount), so the
    assertion is a subset, not an equality.
    """
    from luna.utils.constant import EDITOR_KEYS
    from luna.utils.helper import Helper
    path_or_inline = set(Helper.PATH_OR_INLINE_KEYS)
    assert not path_or_inline & FREE_TEXT_KEYS, 'a key cannot be both'
    unclassified = set(EDITOR_KEYS) - path_or_inline - FREE_TEXT_KEYS
    assert not unclassified, (
        f'{sorted(unclassified)} is a new editor key that nobody classified. A value '
        f'that can never legitimately look like a path belongs in '
        f'Helper.PATH_OR_INLINE_KEYS; otherwise add it to FREE_TEXT_KEYS with the '
        f'reason a path-like value is legitimate for it'
    )


def test_addmount_reports_the_missing_file_not_the_entry_shape(helper, capsys):
    """addmount -qmnt with a path that does not exist names the file.

    Without the guard the path string reaches the mounts parser and the user is told
    "a mount entry must be an object with a path", which is about the wrong thing.
    """
    with pytest.raises(SystemExit):
        helper.add_mount(table='node', args={'name': 'qa-node', 'mount': '/tmp/no-such-mount.yml'})
    err = capsys.readouterr().err
    assert '/tmp/no-such-mount.yml' in err
    assert 'does not exist' in err
