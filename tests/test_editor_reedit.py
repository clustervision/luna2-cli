#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
A refused editor change goes back to the editor with the reason on top, instead of
being thrown away. Refused by the CLI (a document that does not parse) or by the
daemon at store time, for any field that was edited; declined or without a terminal,
the command still fails, and the edit is kept and its path printed.
"""

import base64
import json
import logging
import os
import types

import pytest

import luna.utils.helper as helper_module
import luna.utils.log as luna_log
from luna.utils.helper import Helper

GOOD = 'version: 2\nsets:\n- {name: os, role: os, raid: none, volumes: []}\n'
FIXED = 'version: 2\nsets:\n- {name: os, role: os, raid: "1", volumes: []}\n'
BROKEN = 'version: 2\nsets: [\n'


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


@pytest.fixture(name='editor')
def editor_fixture(monkeypatch):
    """An editor that types the next text and records what it was shown."""
    state = {'texts': [], 'shown': []}

    def call(args):
        filename = args[1]
        with open(filename, 'r', encoding='utf-8') as handle:
            shown = handle.read()
        state['shown'].append(shown)
        marks = ''.join(line for line in shown.splitlines(keepends=True)
                        if line.startswith(Helper.REFUSAL_MARK))
        with open(filename, 'w', encoding='utf-8') as handle:
            handle.write(marks + state['texts'].pop(0))
        return 0

    monkeypatch.setattr(helper_module.subprocess, 'call', call)
    return state


def _terminal(monkeypatch, answers):
    monkeypatch.setattr(helper_module.sys.stdin, 'isatty', lambda: True)
    monkeypatch.setattr('builtins.input', lambda prompt: answers.pop(0))


def _no_terminal(monkeypatch):
    monkeypatch.setattr(helper_module.sys.stdin, 'isatty', lambda: False)

    def no_prompt(prompt):
        raise AssertionError('prompted without a terminal')
    monkeypatch.setattr('builtins.input', no_prompt)


def _decoded(value):
    return base64.b64decode(value).decode('utf-8')


def test_a_document_that_does_not_parse_is_edited_again(editor, monkeypatch):
    editor['texts'] = [BROKEN, GOOD]
    _terminal(monkeypatch, ['y'])
    value = Helper().open_editor('disklayout', None, {})
    assert json.loads(_decoded(value))['sets'][0]['name'] == 'os'
    assert len(editor['shown']) == 2
    assert editor['shown'][1].startswith(Helper.REFUSAL_MARK + 'invalid disklayout')
    assert BROKEN in editor['shown'][1], 'the second edit did not start from the operator\'s text'


@pytest.mark.parametrize('answer', ['n', None])
def test_a_declined_or_scripted_edit_fails_and_keeps_the_file(editor, monkeypatch, capsys, answer):
    editor['texts'] = [BROKEN]
    if answer is None:
        _no_terminal(monkeypatch)
    else:
        _terminal(monkeypatch, [answer])
    with pytest.raises(SystemExit) as stop:
        Helper().open_editor('disklayout', None, {})
    assert stop.value.code != 0
    printed = capsys.readouterr().err
    kept = printed.split('Your edit is kept in ')[1].split()[0].rstrip('.')
    with open(kept, 'r', encoding='utf-8') as handle:
        assert BROKEN in handle.read()
    os.remove(kept)
    os.rmdir(os.path.dirname(kept))


class FakeDaemon():
    """The record exists; each post answers the next response."""

    def __init__(self, answers):
        self.answers = answers
        self.posted = []

    def __call__(self):
        return self

    def get_data(self, table=None, name=None):
        return types.SimpleNamespace(status_code=200, content={})

    def post_data(self, table=None, name=None, data=None):
        self.posted.append(data)
        code, content = self.answers.pop(0)
        return types.SimpleNamespace(status_code=code, content=content)


def _change(monkeypatch, key, answers):
    """luna node change node001 -e <key>, against a daemon that answers in turn."""
    daemon = FakeDaemon(answers)
    monkeypatch.setattr(helper_module, 'Rest', daemon)

    def prepare(self, table=None, data=None, local=False):
        return {'name': 'node001', key: self.open_editor(key, None, {'name': 'node001'})}
    monkeypatch.setattr(Helper, 'prepare_payload', prepare)
    Helper().update_record('node', {'name': 'node001'})
    return daemon


@pytest.mark.parametrize('key, first, second', [
    ('disklayout', GOOD, FIXED),
    ('prescript', 'echo one\n', 'echo two\n'),
])
def test_a_change_the_daemon_refuses_is_edited_again(editor, monkeypatch, key, first, second):
    editor['texts'] = [first, second]
    _terminal(monkeypatch, ['y'])
    daemon = _change(monkeypatch, key, [(400, 'refused for a reason'), (204, '')])
    assert len(daemon.posted) == 2
    assert editor['shown'][1].startswith(Helper.REFUSAL_MARK + 'refused for a reason')
    stored = _decoded(daemon.posted[1]['config']['node']['node001'][key])
    assert Helper.REFUSAL_MARK not in stored, 'the reason reached the daemon'
    if key == 'prescript':
        assert stored == second


def test_a_stored_change_leaves_no_file_behind(editor, monkeypatch):
    editor['texts'] = [GOOD]
    _terminal(monkeypatch, [])
    before = {name for name in os.listdir('/tmp') if name.startswith('lunatmp-')}
    _change(monkeypatch, 'disklayout', [(204, '')])
    after = {name for name in os.listdir('/tmp') if name.startswith('lunatmp-')}
    assert after == before
