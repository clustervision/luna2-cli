#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
The completion file has to know what the parser offers, and it has to keep its tail.

Two failures, both of which have happened and neither of which announces itself.

A subcommand added to the parser and not to the completion still works -- it simply
does not complete, and nobody notices until an operator types it in full. That is the
generic CLI bug shape here: two hand-written lists over the same thing, drifting.

The tail is worse. Below the generated shtab block sit ~85 hand-appended lines of
argcomplete, and they are what makes completion *dynamic* -- real node names, real
group names, computed live against the daemon. Bash keeps the last `complete`
registration for a command, so the tail is the only completer that actually runs.
A regeneration that eats it leaves a file that still looks like a working completion:
subcommands complete from the static tree, and only live values quietly stop. A commit
once took this file from ten argcomplete references to zero and passed review.

Both are checked by deriving from the source rather than by naming anything, so the
next entity and the next verb are covered without anyone remembering this file exists.
"""

import ast
import os
import re

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES = os.path.join(ROOT, 'luna')
COMPLETION = os.path.join(MODULES, 'addons', 'bash_completion.sh')


@pytest.fixture(scope='module')
def completion():
    with open(COMPLETION, 'r', encoding='utf-8') as handle:
        return handle.read()


def _entity_modules():
    for entry in sorted(os.listdir(MODULES)):
        if entry.endswith('.py') and entry not in ('__init__.py', 'cli.py'):
            yield entry


def _literal_verbs(filename):
    """
    The verbs registered with a literal add_parser('name'). Entities that build their
    subcommands from a constant in a loop -- service does, from SERVICES -- yield
    nothing here, and are skipped rather than guessed at.
    """
    with open(os.path.join(MODULES, filename), 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    verbs = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != 'add_parser' or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            verbs.add(first.value)
    # scope sub-parsers (node/group/cluster under secrets) are not verbs
    return verbs - {'node', 'group', 'cluster'}


def _array(completion, name):
    match = re.search(rf"{re.escape(name)}=\(([^)]*)\)", completion)
    if not match:
        return None
    return {item.strip("'") for item in match.group(1).split()}


# --- the parser and the completion describe the same tree -------------------

@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_command_is_offered_at_the_top_level(filename, completion):
    """A command the completion has never heard of does not complete at all."""
    entity = filename[:-3]
    commands = _array(completion, '_shtab_luna_subparsers')
    assert commands is not None, 'the completion has no top-level subparser list'
    assert entity in commands, (
        f'`luna {entity}` exists but is not in the completion. Regenerate on a '
        f'controller with a working luna, keeping the header and the tail.'
    )


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_verb_the_parser_offers_can_be_completed(filename, completion):
    """
    Only the missing direction is asserted. A verb you can type but cannot complete
    is the failure this catches; a stale extra in the completion is harmless by
    comparison, and asserting on it would fail on entities whose verbs are built
    dynamically.
    """
    entity = filename[:-3]
    wanted = _literal_verbs(filename)
    if not wanted:
        pytest.skip(f'{filename} builds its subcommands dynamically')
    offered = _array(completion, f'_shtab_luna_{entity}_subparsers')
    assert offered is not None, f'the completion has no subparser list for {entity}'
    missing = sorted(wanted - offered)
    assert not missing, f'{entity}: {missing} can be typed but will not complete'


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_the_positional_choices_agree_with_the_subparser_list(filename, completion):
    """The same verbs appear twice in this file, and the two copies drift."""
    entity = filename[:-3]
    offered = _array(completion, f'_shtab_luna_{entity}_subparsers')
    choices = _array(completion, f'_shtab_luna_{entity}_pos_0_choices')
    if offered is None or choices is None:
        pytest.skip(f'{entity} has no paired lists in the completion')
    assert offered == choices, (
        f'{entity}: subparsers and pos_0_choices disagree - '
        f'{sorted(offered ^ choices)}'
    )


# --- the tail, which is the one that fails silently -------------------------

def test_the_dynamic_completion_tail_is_still_there(completion):
    """
    Ten references, which is what a whole argcomplete tail looks like. Zero is what
    a naive regeneration leaves behind, and the file still reads as a working
    completion afterwards.
    """
    assert completion.count('_python_argcomplete') == 10, (
        'the hand-appended argcomplete tail has been damaged. Live values - node '
        'names, group names - will silently stop completing while subcommands '
        'carry on working.'
    )


def test_argcomplete_registers_last_so_it_is_the_completer_that_runs(completion):
    """
    Bash keeps the *last* `complete` registration for a command. The shtab block
    registers _shtab_luna and the tail then overrides it with _python_argcomplete;
    reverse the order and the static tree wins, which looks fine and completes no
    live value at all.
    """
    registrations = re.findall(r'complete\s+.*-F\s+(\S+)\s+luna', completion)
    assert registrations, 'no complete registration found at all'
    assert registrations[-1] == '_python_argcomplete', (
        f'the last completer registered is {registrations[-1]}, not _python_argcomplete'
    )


def test_the_hand_written_header_survives(completion):
    """The licence header and the install note are hand-written and in no generator's output."""
    assert 'GNU General Public License' in completion
    assert 'Copy this file as /etc/bash_completion.d/luna' in completion
    assert 'AUTOMATICALLY GENERATED by `shtab`' in completion


def test_the_completion_is_valid_shell(completion):
    """A stray print while the parser is built lands on line 1 and the shell executes it."""
    import subprocess
    result = subprocess.run(['bash', '-n', COMPLETION], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


# --- the flags, not just the verbs ------------------------------------------

ARGUMENTS = os.path.join(MODULES, 'utils', 'arguments.py')


def _option_strings_of(call):
    """The dashed option strings of one add_argument call, ignoring positionals."""
    return {a.value for a in call.args
            if isinstance(a, ast.Constant) and isinstance(a.value, str)
            and a.value.startswith('-')}


def _shared_arg_helpers():
    """
    {helper name: {flags it adds}} from utils/arguments.py. Entities do not spell
    most of their flags out - they call common_bmcsetup_args(parser) and friends -
    so a test that only walked the entity module would see almost nothing.
    """
    with open(ARGUMENTS, 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    helpers = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        # Only what the helper adds unconditionally. common_list_args adds --csv
        # inside `if csv:`, so it exists for `list` and not for `show`, and
        # counting it for every caller would report a flag that is not offered.
        flags = set()
        for inner in node.body:
            for call in ast.walk(inner):
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                        and call.func.attr == 'add_argument'
                        and not isinstance(inner, ast.If)):
                    flags |= _option_strings_of(call)
        if flags:
            helpers[node.name] = flags
    return helpers


def _flags_by_verb(filename):
    """
    {verb: {flags}} for one entity module, following both the flags added straight
    onto a verb's parser and the shared helpers that parser is handed to.
    """
    with open(os.path.join(MODULES, filename), 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    helpers = _shared_arg_helpers()
    variable_verb = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and node.value.func.attr == 'add_parser'
                and node.value.args
                and isinstance(node.value.args[0], ast.Constant)):
            variable_verb[node.targets[0].id] = node.value.args[0].value
    flags = {verb: set() for verb in variable_verb.values()}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        # verb_parser.add_argument('-x', '--yy')
        if (node.func.attr == 'add_argument' and isinstance(node.func.value, ast.Name)
                and node.func.value.id in variable_verb):
            flags[variable_verb[node.func.value.id]] |= _option_strings_of(node)
        # Arguments().common_something_args(verb_parser)
        elif node.func.attr in helpers and node.args:
            first = node.args[0]
            if isinstance(first, ast.Name) and first.id in variable_verb:
                flags[variable_verb[first.id]] |= helpers[node.func.attr]
    return flags


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_flag_the_parser_offers_can_be_completed(filename, completion):
    """
    The verbs were checked and the flags were not, so a new option could be added
    to the parser and this file stayed green while the flag silently did not
    complete. That is how --cipher on bmcsetup shipped uncompletable.

    Only the missing direction is asserted, as with the verbs: a flag you can type
    but cannot complete is the failure worth catching, while a stale extra in the
    completion is harmless and would fail on anything built dynamically.
    """
    entity = filename[:-3]
    by_verb = _flags_by_verb(filename)
    if not by_verb:
        pytest.skip(f'{filename} builds its subcommands dynamically')
    problems = []
    for verb, wanted in sorted(by_verb.items()):
        if not wanted:
            continue
        offered = _array(completion, f'_shtab_luna_{entity}_{verb}_option_strings')
        if offered is None:
            continue          # the verb itself is missing - the verb test says so
        missing = sorted(wanted - offered)
        if missing:
            problems.append(f'{entity} {verb}: {missing}')
    assert not problems, (
        'these flags can be typed but will not complete:\n  ' + '\n  '.join(problems)
        + '\nSplice them into the matching _option_strings array. Do not regenerate '
          'the whole file: it needs a live daemon, it bakes that box\'s controller '
          'hostnames in as literal option strings, and it drops flags the generating '
          'box\'s package does not have.'
    )
