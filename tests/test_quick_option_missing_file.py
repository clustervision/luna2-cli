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

"""-qdl, -qmnt and -qof take a file path or the document in-line. A value that
plainly is a path but does not exist used to be taken as in-line JSON, failed as
"disklayout must be an object, got a str", and the whole change (other options
on the same command line included) was dropped. Helper.looks_like_missing_file
tells the two apart."""

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


@pytest.mark.parametrize("key", ["disklayout", "mounts", "osimage_filter"])
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
