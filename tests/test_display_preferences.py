#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
TRIX-2211: owners, usergroups and access are an optional CLI display preference.

Every governed list and show keeps its existing fields by default. A personal
setting overrides the controller's, raw answers keep all their data, and access
commands and user memberships remain available when the columns are hidden.
"""

from configparser import RawConfigParser
from copy import deepcopy
import importlib
import logging
import types

import pytest

from luna.utils.constant import ACCESS_FIELDS, GOVERNED_TABLES
from luna.utils.display import Display
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.rest import Rest


@pytest.fixture(autouse=True)
def config(tmp_path, monkeypatch):
    """
    Isolate personal and controller preferences and reset the per-command cache.
    """
    import luna.utils.display as display
    personal = tmp_path / 'home' / '.luna' / 'luna.ini'
    controller = tmp_path / 'controller' / 'luna.ini'
    personal.parent.mkdir(parents=True)
    controller.parent.mkdir()
    monkeypatch.setattr(display, 'USER_INI_FILE', str(personal))
    monkeypatch.setattr(display, 'INI_FILE', str(controller))
    monkeypatch.setattr(Log, '_Log__logger', logging.getLogger('luna2-cli-tests'))
    Display.preferences.cache_clear()
    yield types.SimpleNamespace(personal=personal, controller=controller)
    Display.preferences.cache_clear()


def setting(path, value):
    """
    Write only a display section: preferences do not select credentials.
    """
    path.write_text(f'[DISPLAY]\nSHOW_RBAC = {value}\n', encoding='utf-8')


# ------------------------------------------------------- configuration ----

@pytest.mark.parametrize('value, expected', [
    ('yes', True), ('true', True), ('on', True), ('1', True),
    ('no', False), ('false', False), ('off', False), ('0', False), ('NO', False),
])
def test_standard_boolean_values(config, value, expected):
    """
    Use INI boolean parsing rather than the truth value of a nonempty string.
    """
    setting(config.controller, value)
    assert Display.preferences()['SHOW_RBAC'] is expected


@pytest.mark.parametrize('personal, controller', [('yes', 'no'), ('no', 'yes')])
def test_personal_value_wins_over_controller(config, personal, controller):
    """
    Both directions work, including an explicit personal preference to show.
    """
    setting(config.personal, personal)
    setting(config.controller, controller)
    assert Display.preferences()['SHOW_RBAC'] is (personal == 'yes')


def test_missing_personal_option_uses_controller(config):
    """
    A person's login file need not repeat the controller display setting.
    """
    config.personal.write_text('[API]\nUSERNAME = alice\n', encoding='utf-8')
    setting(config.controller, 'no')
    assert Display.preferences()['SHOW_RBAC'] is False


def test_missing_setting_defaults_to_enabled(config):
    """
    Existing installations without a display section retain their output.
    """
    config.controller.write_text('[API]\nUSERNAME = luna\n', encoding='utf-8')
    assert Display.preferences()['SHOW_RBAC'] is True


def test_personal_path_expands_the_home_directory(config, monkeypatch):
    """
    The configured personal path follows the person running this CLI process.
    """
    import luna.utils.display as display
    monkeypatch.setenv('HOME', str(config.personal.parent.parent))
    monkeypatch.setattr(display, 'USER_INI_FILE', '~/.luna/luna.ini')
    setting(config.personal, 'no')
    assert Display.preferences()['SHOW_RBAC'] is False


def test_missing_files_default_to_enabled():
    """
    Display preferences are optional and never demand a login file.
    """
    assert Display.preferences()['SHOW_RBAC'] is True


@pytest.mark.parametrize('value', ['', 'perhaps'])
def test_invalid_value_warns_once_and_defaults_to_enabled(config, capsys, value):
    """
    An invalid personal value does not accidentally inherit a hidden default.
    """
    setting(config.personal, value)
    setting(config.controller, 'no')
    assert Display.preferences()['SHOW_RBAC'] is True
    assert Display.preferences()['SHOW_RBAC'] is True
    assert capsys.readouterr().err.count('Invalid [DISPLAY] SHOW_RBAC') == 1


@pytest.mark.parametrize('content', [b'not an INI file', b'\xff',
                                    b'[DISPLAY]\nSHOW_RBAC = no\nSHOW_RBAC = yes\n'])
def test_malformed_personal_file_uses_controller(config, capsys, content):
    """
    A parse failure is contained, without printing the file's possibly secret text.
    """
    config.personal.write_bytes(content)
    setting(config.controller, 'no')
    assert Display.preferences()['SHOW_RBAC'] is False
    warning = capsys.readouterr().err
    assert 'Cannot read display preferences' in warning
    assert 'not an INI file' not in warning


def test_unreadable_personal_file_uses_controller(config, monkeypatch):
    """
    Permission failures are simulated so this also runs as root on a controller.
    """
    setting(config.personal, 'yes')
    setting(config.controller, 'no')
    original = RawConfigParser.read

    def read(self, filename, **kwargs):
        if filename == str(config.personal):
            raise PermissionError('unreadable')
        return original(self, filename, **kwargs)

    monkeypatch.setattr(RawConfigParser, 'read', read)
    assert Display.preferences()['SHOW_RBAC'] is False


def test_preferences_are_read_once_per_process(config, monkeypatch):
    """
    Several tables in one command do not keep opening both INI files.
    """
    setting(config.controller, 'no')
    original = RawConfigParser.read
    calls = []

    def read(self, filename, **kwargs):
        calls.append(filename)
        return original(self, filename, **kwargs)

    monkeypatch.setattr(RawConfigParser, 'read', read)
    for table in ['node', 'group', 'profile']:
        Display.filter_fields(table, ['name', 'access'], [['item', 'rwx------']])
    assert calls == [str(config.personal), str(config.controller)]


def test_reporting_an_invalid_setting_cannot_break_the_command(config, monkeypatch):
    """
    A closed stderr cannot turn an optional preference into a command failure.
    """
    import luna.utils.display as display
    setting(config.personal, 'invalid')

    def write(message):
        raise ValueError('I/O operation on closed file')

    monkeypatch.setattr(display, 'sys', types.SimpleNamespace(stderr=types.SimpleNamespace(write=write)))
    assert Display.preferences()['SHOW_RBAC'] is True


# ------------------------------------------------------ governed views ----

ENTITIES = [
    ('node', 'Node'), ('group', 'Group'), ('osimage', 'OSImage'),
    ('bmcsetup', 'BMCSetup'), ('redfishsetup', 'RedfishSetup'),
    ('biosconfig', 'BiosConfig'), ('firmwarecatalog', 'FirmwareCatalog'),
    ('profile', 'Profile'), ('network', 'Network'), ('cloud', 'Cloud'),
    ('switch', 'Switch'), ('otherdev', 'OtherDev'), ('route', 'Network'),
    ('cluster', 'Cluster'),
]


def run_view(monkeypatch, entity, class_name, action, raw=False):
    """
    Run the real entity method and Presenter against a fake daemon transport.
    """
    module = importlib.import_module('luna.network' if entity == 'route' else 'luna.' + entity)
    cls = getattr(module, class_name)
    command = cls.__new__(cls)
    command.table = entity
    command.table_cap = entity.capitalize()
    command.route = 'profiles' if entity == 'profile' else entity
    command.logger = logging.getLogger('luna2-cli-tests')
    command.args = {'name': 'item', 'raw': raw, 'settings': False}
    if entity == 'cluster':
        command.args.pop('name')
    record = {'name': 'item', 'owners': 'alice', 'usergroups': 'physics', 'access': 'rwxr-x---',
              'interfaces': [], 'files': [], 'scope': 'static', 'service': 'chronyd',
              'action': 'restart', 'comment': None, 'future_field': 'still-visible'}
    key = 'profiles' if entity == 'profile' else entity

    def get_data(self, table, name=None, **kwargs):
        detail = deepcopy(record)
        # Profiles encode the name in the route; cluster is a singleton.
        data = detail if entity == 'cluster' and action == 'show' else {'item': detail}
        return types.SimpleNamespace(status_code=200, content={'config': {key: data}})

    monkeypatch.setattr(Rest, '__init__', lambda self: None)
    monkeypatch.setattr(Rest, 'get_data', get_data)
    method = f'{action}_{entity}'
    if entity == 'route':
        method = f'network_route_{action}'
    elif entity == 'cluster':
        method = 'cluster_info'
    getattr(command, method)()
    return record


@pytest.mark.parametrize('entity, class_name', ENTITIES)
@pytest.mark.parametrize('action', ['list', 'show'])
@pytest.mark.parametrize('value', ['yes', 'no', None])
def test_each_governed_view_honours_the_setting(config, monkeypatch, capsys,
                                                entity, class_name, action, value):
    """
    Check actual terminal output, including custom node, profile and BIOS views.
    """
    if entity == 'cluster' and action == 'list':
        pytest.skip('Cluster is a singleton with a show command only')
    if value is not None:
        setting(config.personal, value)
    run_view(monkeypatch, entity, class_name, action)
    output = capsys.readouterr().out
    assert 'item' in output
    for field in ACCESS_FIELDS:
        assert (field in output) is (value != 'no'), (entity, action, field, output)
    if action == 'show' and entity not in ('profile',):
        assert 'future_field' in output, 'Unregistered show fields must remain visible'


@pytest.mark.parametrize('entity, class_name', ENTITIES)
@pytest.mark.parametrize('action', ['list', 'show'])
def test_raw_views_keep_access_fields(config, monkeypatch, capsys, entity, class_name, action):
    """
    The same commands bypass display filtering for raw answers.
    """
    if entity == 'cluster' and action == 'list':
        pytest.skip('Cluster is a singleton with a show command only')
    setting(config.personal, 'no')
    monkeypatch.setattr(Display, 'filter_fields', lambda *a, **k: pytest.fail('Raw output was filtered'))
    run_view(monkeypatch, entity, class_name, action, raw=True)
    output = capsys.readouterr().out
    for field in ACCESS_FIELDS:
        assert f'"{field}"' in output
    assert 'alice' in output and 'rwxr-x---' in output


@pytest.mark.parametrize('entity', GOVERNED_TABLES)
@pytest.mark.parametrize('column', [False, True])
def test_field_groups_cover_aliases_and_preserve_input(config, entity, column):
    """
    Also cover governed aliases and rack, which has no standalone CLI command.
    """
    setting(config.personal, 'no')
    fields = ['name', 'owners', 'usergroups', 'access *', 'future_field']
    values = ['item', 'alice', 'physics', 'rwxr-x---', 'unchanged']
    rows = values if column else [values, list(values)]
    original = deepcopy((fields, rows))
    filtered_fields, filtered_rows = Display.filter_fields(entity, fields, rows, column)
    assert filtered_fields == ['name', 'future_field']
    expected = ['item', 'unchanged'] if column else [['item', 'unchanged']] * 2
    assert filtered_rows == expected
    assert (fields, rows) == original


def test_another_field_group_reuses_the_same_filter(config, monkeypatch):
    """
    A future preference needs a field group, without another command-specific branch.
    """
    import luna.utils.display as display
    monkeypatch.setitem(display.DISPLAY_FIELD_GROUPS, 'SHOW_COMMENT', ('comment',))
    setting(config.personal, 'yes')
    config.controller.write_text('[DISPLAY]\nSHOW_RBAC = no\nSHOW_COMMENT = no\n', encoding='utf-8')
    fields, rows = Display.filter_fields('node', ['name', 'comment', 'access'], [['item', 'hidden', 'rwx------']])
    assert fields == ['name', 'access']
    assert rows == [['item', 'rwx------']]


# ------------------------------------------------------- unchanged paths ----

def test_user_memberships_and_explicit_access_reports_remain(config, monkeypatch, capsys):
    """
    A field called usergroups or access is not hidden outside governed views.
    """
    setting(config.personal, 'no')
    fields, rows = Helper().filter_data('user', {'alice': {'username': 'alice', 'usergroups': {'physics': 'operator'}}})
    assert 'usergroups' in fields
    assert 'physics (operator)' in rows[0]
    from luna.user import User
    command = User.__new__(User)
    command.args = {'name': 'alice', 'raw': False}
    monkeypatch.setattr(Rest, '__init__', lambda self: None)
    monkeypatch.setattr(Rest, 'get_raw', lambda *a, **k: types.SimpleNamespace(status_code=200, json=lambda:
                        {'config': {'user': {'alice': {'access': {'node': {'item': 'r-x'}}}}}}))
    command.access_user()
    output = capsys.readouterr().out
    assert 'access' in output and 'r-x (read, operate)' in output


def test_access_changes_still_send_the_complete_payload(config, monkeypatch):
    """
    SHOW_RBAC does not remove fields from a write request.
    """
    setting(config.personal, 'no')
    from luna.access import Access
    command = Access.__new__(Access)
    command.args = {'entity': 'node', 'name': 'item', 'access': '750'}
    posted = []
    monkeypatch.setattr(Rest, '__init__', lambda self: None)
    monkeypatch.setattr(Rest, 'post_raw', lambda self, path, data:
                        posted.append((path, data)) or types.SimpleNamespace(status_code=204))
    command.chmod_access()
    assert posted == [('config/node/item/_chmod', {'config': {'node': {'item': {'access': '750'}}}})]


def test_explicit_csv_column_is_not_hidden(config, capsys):
    """
    A script explicitly requesting one column still receives its values.
    """
    setting(config.personal, 'no')
    Helper().column_csv('node', {'item': {'owners': 'alice'}}, 'owners')
    assert capsys.readouterr().out == 'alice\n'


def test_whoami_keeps_the_usergroup_roles(config, monkeypatch, capsys):
    """
    The identity report remains useful when ordinary object columns are hidden.
    """
    setting(config.personal, 'no')
    from luna.access import Access
    command = Access.__new__(Access)
    command.args = {'raw': False}
    monkeypatch.setattr(Rest, '__init__', lambda self: None)
    monkeypatch.setattr(Rest, 'get_raw', lambda *a, **k: types.SimpleNamespace(status_code=200, json=lambda:
                        {'user': 'alice', 'id': 7, 'source': 'local', 'admin': False,
                         'usergroups': {'physics': 'operator'}}))
    command.whoami_access()
    output = capsys.readouterr().out
    assert 'usergroups' in output and 'physics (operator)' in output


@pytest.mark.parametrize('previous', ['[DISPLAY]\nSHOW_RBAC = no\n', 'malformed old file'])
def test_logging_in_preserves_valid_preferences_and_repairs_invalid_files(config, monkeypatch, previous):
    """
    A fresh login retains display settings without being blocked by a broken old INI.
    """
    import luna.access as access
    config.personal.write_text(previous, encoding='utf-8')
    monkeypatch.setattr(access, 'USER_INI_FILE', str(config.personal))
    monkeypatch.setattr(access, 'USER_TOKEN_FILE', str(config.personal.parent / 'token'))
    monkeypatch.setattr(access, 'getpass', lambda *a: 'password')
    monkeypatch.setattr(access.Access, '_controller_endpoint', lambda self: ('ctrl:7050', 'https', 'no'))
    monkeypatch.setattr(access, 'Rest', lambda: types.SimpleNamespace(ini_file=str(config.personal), token=lambda: 'token'))
    command = access.Access.__new__(access.Access)
    command.args = {'username': 'alice'}
    command.login_access()
    parser = RawConfigParser()
    parser.read(config.personal)
    assert parser.get('API', 'USERNAME') == 'alice'
    if previous.startswith('[DISPLAY]'):
        assert parser.getboolean('DISPLAY', 'SHOW_RBAC') is False
