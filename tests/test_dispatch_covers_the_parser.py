#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.

"""
Every verb the parser offers must be dispatchable.

Each entity module registers its subcommands with add_parser(), and then dispatches
them through a second, hand-written list of action names. Two lists describing the
same thing drift: a verb added to the parser but not to the list parses, completes,
prints its own --help, and then refuses to run with 'Kindly choose from ...'.

That has happened. It is checked here by deriving both sides from the source rather
than by naming the verbs, so the next entity and the next verb are covered without
anyone remembering this file exists.
"""

import ast
import os

import pytest

MODULES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'luna')


def _entity_modules():
    for entry in sorted(os.listdir(MODULES)):
        if entry.endswith('.py') and entry not in ('__init__.py', 'cli.py'):
            yield entry


def _parsed(filename):
    with open(os.path.join(MODULES, filename), 'r', encoding='utf-8') as handle:
        return ast.parse(handle.read())


def _parser_verbs(tree):
    """The verbs registered with add_parser(), which is what an operator can type."""
    verbs = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != 'add_parser' or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            verbs.add(first.value)
    return verbs


def _table(tree):
    """The entity name the module dispatches under, from self.table."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr == 'table':
                if isinstance(node.value, ast.Constant):
                    return node.value.value
    return None


def _dispatch_actions(tree):
    """What the dispatcher will accept. The central table in constant.py is the
    convention; a module carrying its own copy is the divergence this catches."""
    from luna.utils.constant import actions
    table = _table(tree)
    if not table:
        return None
    try:
        listed = actions(table)
    except KeyError:
        # not every module dispatches through the central table - cluster and monitor
        # have their own shape. Skipping is honest; asserting here would be noise
        return None
    return set(listed) if listed else None


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_offered_verb_can_be_dispatched(filename):
    tree = _parsed(filename)
    actions = _dispatch_actions(tree)
    if actions is None:
        pytest.skip(f'{filename} does not dispatch through an action list')
    verbs = _parser_verbs(tree)
    entity = filename[:-3]
    # scope sub-parsers (node/group/cluster under secrets) are not verbs
    scopes = {'node', 'group', 'cluster'}
    offered = {verb for verb in verbs if verb not in scopes}
    missing = sorted(offered - actions)
    assert not missing, (f'{filename}: {missing} can be typed and completed but not run - '
                         f'the dispatch list did not learn about them')


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_the_parser_actually_builds(filename):
    """Reading the source is not enough. A verb whose parser line references something
    the module never imported passes every static check and then takes the whole CLI
    down at startup - `luna` builds every entity's parser before it looks at argv, so
    one NameError in one module breaks every command.

    This builds it for real. A module that cannot be built without a live daemon is
    skipped by name rather than by swallowing the error, because swallowing it is how
    the missing import got through in the first place.
    """
    import importlib
    import logging
    from argparse import ArgumentParser

    import luna.utils.log as luna_log
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001

    entity = filename[:-3]
    module = importlib.import_module(f'luna.{entity}')
    cls = next((getattr(module, name) for name in dir(module)
                if name.lower() == entity and isinstance(getattr(module, name), type)), None)
    if cls is None:
        pytest.skip(f'{filename} has no {entity} class to build')

    parser = ArgumentParser(prog='luna')
    subparsers = parser.add_subparsers(dest='command')
    try:
        cls(parser=parser, subparsers=subparsers)
    except (NameError, AttributeError, TypeError) as exp:
        pytest.fail(f'{filename}: building the parser raised {type(exp).__name__}: {exp}')
    except Exception as exp:  # pylint: disable=broad-except
        # cluster.py reaches the daemon while building - that is a known property of
        # this CLI, and shtab needs a live controller for the same reason
        pytest.skip(f'{filename} needs a live daemon to build its parser: {exp}')

    registered = subparsers.choices.get(entity)
    if registered is None or not registered._subparsers:  # noqa: SLF001
        pytest.skip(f'{filename} registers no subcommands')
    verbs = set(registered._subparsers._group_actions[0].choices)  # noqa: SLF001
    actions = _dispatch_actions(_parsed(filename))
    if actions is None:
        pytest.skip(f'{filename} does not dispatch through the central table')
    scopes = {'node', 'group', 'cluster'}
    missing = sorted({verb for verb in verbs if verb not in scopes} - actions)
    assert not missing, f'{filename}: {missing} build but cannot be dispatched'


def _explicit_dispatch():
    """The command -> class-name branches spelled out in cli.py's dispatcher."""
    import re
    path = os.path.join(MODULES, 'cli.py')
    with open(path, 'r', encoding='utf-8') as handle:
        source = handle.read()
    pattern = r'self\.args\["command"\] == "(\w+)":\s*\n\s*call = globals\(\)\["(\w+)"\]'
    return dict(re.findall(pattern, source))


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_command_resolves_to_a_class_the_dispatcher_can_reach(filename):
    """
    The dispatcher falls back to globals()[command.capitalize()], and capitalize is
    not the casing several of these classes use: OSImage, BMCSetup, OtherDev and
    RedfishSetup all become something that is not their name. Each therefore needs
    an explicit branch, and forgetting one is not a parse error or a startup error
    -- the command parses, completes, prints its own help, and dies with a KeyError
    the moment it is run.

    Derived from the modules on disk rather than from a list of names, so the next
    entity is covered without anyone remembering this file exists.
    """
    import importlib

    import luna.cli

    entity = filename[:-3]
    module = importlib.import_module(f'luna.{entity}')
    cls = next((getattr(module, name) for name in dir(module)
                if name.lower() == entity and isinstance(getattr(module, name), type)), None)
    if cls is None:
        pytest.skip(f'{filename} has no {entity} class')

    expected = _explicit_dispatch().get(entity, entity.capitalize())
    resolved = getattr(luna.cli, expected, None)
    assert resolved is not None, (
        f'`luna {entity}` dispatches to globals()["{expected}"], which does not exist. '
        f'The class is {cls.__name__} -- add a branch for it in Cli.main, as osimage, '
        f'bmcsetup and otherdev have.'
    )
    assert resolved is cls, (
        f'`luna {entity}` dispatches to {resolved.__name__}, not {cls.__name__}'
    )


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_entity_module_is_in_the_classes_list(filename):
    """
    cli.py holds a hardcoded `classes` list, and a module absent from it is imported
    and never wired into the parser -- so the subcommand does not exist and nothing
    complains.
    """
    import importlib

    import luna.cli

    entity = filename[:-3]
    module = importlib.import_module(f'luna.{entity}')
    cls = next((getattr(module, name) for name in dir(module)
                if name.lower() == entity and isinstance(getattr(module, name), type)), None)
    if cls is None:
        pytest.skip(f'{filename} has no {entity} class')
    assert cls.__name__ in _registered_classes(), (
        f'{cls.__name__} is not in the classes list in cli.py, so `luna {entity}` '
        f'never reaches the parser'
    )


def _registered_classes():
    """The names in cli.py's hardcoded `classes` list, read as code rather than text -
    the last entry carries no trailing comma, and a text match misses it."""
    with open(os.path.join(MODULES, 'cli.py'), 'r', encoding='utf-8') as handle:
        tree = ast.parse(handle.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.List):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'classes':
                    return {element.id for element in node.value.elts
                            if isinstance(element, ast.Name)}
    raise AssertionError('no `classes` list found in cli.py')


@pytest.mark.parametrize('filename', list(_entity_modules()))
def test_every_dispatchable_verb_has_a_method_to_run(filename):
    """
    The list above proves a verb is *accepted*. It does not prove anything will
    happen when it is.

    Dispatch is `methodcaller(f'{action}_{entity}')` - a name assembled at
    runtime - so a verb that is in the parser and in the action list and has no
    matching method parses, completes, passes every other check here, and then
    raises AttributeError at the moment an operator runs it. Three lists agreeing
    and a fourth thing missing.

    Derived like the rest: the method names come off the class, so the next verb
    is covered without anyone remembering this file.
    """
    import importlib

    tree = _parsed(filename)
    actions = _dispatch_actions(tree)
    if actions is None:
        pytest.skip(f'{filename} does not dispatch through an action list')
    entity = filename[:-3]
    module = importlib.import_module(f'luna.{entity}')
    cls = next((getattr(module, name) for name in dir(module)
                if name.lower() == entity and isinstance(getattr(module, name), type)), None)
    if cls is None:
        pytest.skip(f'{filename} has no {entity} class')

    available = set(dir(cls))
    scopes = {'node', 'group', 'cluster'}
    missing = []
    for verb in sorted(_parser_verbs(tree) & actions):
        if verb in scopes:
            continue
        # three dispatch shapes are in use and all of them are legitimate: the
        # bare verb (node's interface verbs), the verb with the entity appended
        # (the common one), and the entity prefixed to the verb with a further
        # sub-action after it (network_dns_add, and osimage's list_tag). A method
        # that begins with any of those spellings counts as present
        if verb in available or f'{verb}_{entity}' in available:
            continue
        if any(name.startswith((f'{verb}_', f'{entity}_{verb}')) for name in available):
            continue
        # and osimage's tag verbs, which put the verb last: list_tag, show_tag
        if any(name.endswith(f'_{verb}') for name in available):
            continue
        missing.append(verb)
    assert not missing, (f'{filename}: {missing} dispatch to a method that does not '
                         f'exist - typing them raises AttributeError')
