#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
Logging in as oneself (TRIX-2091, the CLI half of TRIX-2121).

The credential file order is the contract: a person's own ~/.luna/luna.ini first, the
controller's file second, and the token cache follows the file that was used, so root on
the controller keeps the shared token exactly as today. The signing key is not needed to
read a token any more: expiry is read unverified, and the daemon decides validity.
"""
import json
import logging
import os
import stat
import time
import types

import pytest
from jwt import encode

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    luna_log.Log._Log__logger = logging.getLogger('test')


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A home directory of our own, and a controller ini we control."""
    monkeypatch.setenv('HOME', str(tmp_path / 'home'))
    os.makedirs(tmp_path / 'home')
    controller_ini = tmp_path / 'controller' / 'luna.ini'
    os.makedirs(controller_ini.parent)
    controller_ini.write_text('[API]\nUSERNAME = luna\nPASSWORD = luna\nENDPOINT = ctrl:7050\n'
                              'PROTOCOL = https\nVERIFY_CERTIFICATE = no\n')
    import luna.utils.rest as rest
    monkeypatch.setattr(rest, 'INI_FILE', str(controller_ini))
    monkeypatch.setattr(rest, 'TOKEN_FILE', str(tmp_path / 'controller' / 'token.txt'))
    import luna.access as access
    monkeypatch.setattr(access, 'INI_FILE', str(controller_ini))
    return types.SimpleNamespace(root=tmp_path, controller_ini=controller_ini,
                                 user_ini=tmp_path / 'home' / '.luna' / 'luna.ini',
                                 user_token=tmp_path / 'home' / '.luna' / 'token')


def _own_login(home, username='alice'):
    os.makedirs(home.user_ini.parent, mode=0o700, exist_ok=True)
    home.user_ini.write_text(f'[API]\nUSERNAME = {username}\nPASSWORD = pw\nENDPOINT = ctrl:7050\n'
                             'PROTOCOL = https\nVERIFY_CERTIFICATE = no\n')


def _token(exp_offset=3600):
    return encode({'id': 7, 'exp': int(time.time()) + exp_offset}, 'a-key-the-client-does-not-have', 'HS256')


# ── the file order ──────────────────────────────────────────────────────────

def test_the_controller_ini_is_used_when_there_is_no_own_login(home):
    from luna.utils.rest import Rest
    rest = Rest()
    assert rest.ini_file == str(home.controller_ini)
    assert rest.token_file.endswith('controller/token.txt'), 'root keeps the shared token as today'
    assert rest.username == 'luna'


def test_the_own_login_is_read_first_and_the_token_follows_it(home):
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    assert rest.ini_file == str(home.user_ini)
    assert rest.token_file == str(home.user_token)
    assert rest.username == 'alice'


def test_neither_file_is_a_clear_refusal_naming_the_login_verb(home, capsys):
    from luna.utils.rest import Rest
    os.remove(home.controller_ini)
    with pytest.raises(SystemExit):
        Rest()
    err = capsys.readouterr().err
    assert 'luna login' in err and str(home.controller_ini) in err


def test_login_and_logout_are_dispatched_without_credentials(home, monkeypatch):
    """A person's first luna login has no ~/.luna yet and cannot read the controller's ini;
    the dispatcher must not demand credentials before the verb that creates them runs.
    Every other verb still passes the check first."""
    from luna import cli as luna_cli
    from luna.utils.rest import Rest
    os.remove(home.controller_ini)
    reached = []
    monkeypatch.setattr(luna_cli, 'Access', lambda args, parser, subparsers: reached.append(args['action']))
    monkeypatch.setattr(luna_cli, 'Node', lambda args, parser, subparsers: reached.append('node'))
    monkeypatch.setattr(Rest, 'daemon_validation', lambda self: reached.append('validated'))
    for action in ('login', 'logout'):
        tool = luna_cli.Cli()
        tool.args = {'command': 'access', 'action': action, 'verbose': None}
        tool.call_class()
    assert reached == ['login', 'logout'], 'no Rest() was built, which would have refused for want of an ini'
    tool = luna_cli.Cli()
    tool.args = {'command': 'node', 'action': 'list', 'verbose': None}
    with pytest.raises(SystemExit):
        tool.call_class()
    assert reached == ['login', 'logout'], 'a listing without any ini is still refused before its verb runs'


def test_the_whole_parser_builds_for_a_person_who_has_not_logged_in(home, monkeypatch):
    """The cluster and network parsers fetch the controller names from the daemon while the
    arguments are being built; without a readable credential file that fetch must yield
    nothing rather than refuse, or luna access login can never be parsed."""
    from luna import cli as luna_cli
    from luna.utils.helper import Helper
    os.remove(home.controller_ini)
    assert Helper().get_controllers() == []
    monkeypatch.setattr(luna_cli.Cli, 'get_version', lambda self: '2.2')
    parser = luna_cli.Cli().get_parser()
    args = vars(parser.parse_args(['access', 'login', 'alice']))
    assert args['command'] == 'access' and args['action'] == 'login' and args['username'] == 'alice'


def test_the_signing_key_is_optional_in_the_ini(home):
    from luna.utils.rest import Rest
    assert Rest().secret_key is None, 'no SECRET_KEY line, no error: the key stays on the daemon'


# ── the token without the key ───────────────────────────────────────────────

def test_a_cached_token_is_accepted_on_its_expiry_alone(home, monkeypatch):
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    os.makedirs(home.user_token.parent, exist_ok=True)
    home.user_token.write_text(_token())
    monkeypatch.setattr(rest, 'token', lambda: pytest.fail('a valid cached token must not trigger a login'))
    assert rest.get_token() == home.user_token.read_text()


def test_an_expired_token_is_renewed_by_logging_in(home, monkeypatch):
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    os.makedirs(home.user_token.parent, exist_ok=True)
    home.user_token.write_text(_token(-10))
    monkeypatch.setattr(rest, 'token', lambda: 'fresh')
    assert rest.get_token() == 'fresh'


def test_a_token_without_an_expiry_claim_is_replaced(home, monkeypatch):
    """A token that says nothing about its expiry cannot be trusted to be current."""
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    os.makedirs(home.user_token.parent, exist_ok=True)
    home.user_token.write_text(encode({'id': 7}, 'k', 'HS256'))
    monkeypatch.setattr(rest, 'token', lambda: 'fresh')
    assert rest.get_token() == 'fresh'


def test_a_stored_token_is_readable_by_its_owner_only(home):
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    rest.store_token('t')
    mode = stat.S_IMODE(os.stat(home.user_token).st_mode)
    assert mode == 0o600, oct(mode)
    assert stat.S_IMODE(os.stat(home.user_token.parent).st_mode) == 0o700


def test_a_token_the_daemon_refuses_is_renewed_once_and_the_call_resent(home, monkeypatch):
    from luna.utils.rest import Rest
    _own_login(home)
    rest = Rest()
    calls = []

    def fake_get(url, **kwargs):
        calls.append(kwargs['headers']['x-access-tokens'])
        return types.SimpleNamespace(status_code=401 if len(calls) == 1 else 200, content=b'{}',
                                     json=lambda: {})
    monkeypatch.setattr(rest.session, 'get', fake_get)
    monkeypatch.setattr(rest, 'get_token', lambda: 'stale')
    monkeypatch.setattr(rest, 'token', lambda: 'renewed')
    response = rest.send('get', 'https://ctrl:7050/config/node')
    assert response.status_code == 200
    assert calls == ['stale', 'renewed']


# ── luna login and logout ───────────────────────────────────────────────────

def test_login_writes_the_own_files_readable_by_the_owner_only(home, monkeypatch):
    from luna.access import Access
    import luna.access as access
    monkeypatch.setattr(access, 'getpass', lambda prompt='': 'pw')
    monkeypatch.setattr(os, 'geteuid', lambda: 1000)
    fetched = []
    monkeypatch.setattr(access.Rest, 'token', lambda self: fetched.append(self.ini_file) or 't')
    Access(args={'action': 'login', 'username': 'alice'})
    assert home.user_ini.exists()
    assert stat.S_IMODE(os.stat(home.user_ini).st_mode) == 0o600
    text = home.user_ini.read_text()
    assert 'username = alice' in text.lower() and 'endpoint = ctrl:7050' in text.lower(), \
        'the endpoint is copied from the controller ini so a person need not know it'
    assert 'secret_key' not in text.lower()
    assert fetched == [str(home.user_ini)], 'the token was fetched through the own file'


def test_root_without_a_username_keeps_the_controller_account(home, monkeypatch, capsys):
    from luna.access import Access
    monkeypatch.setattr(os, 'geteuid', lambda: 0)
    with pytest.raises(SystemExit):
        Access(args={'action': 'login', 'username': None})
    assert 'root already holds the controller account' in capsys.readouterr().err
    assert not home.user_ini.exists(), 'nothing may shadow the break-glass file'


def test_logout_removes_both_own_files(home, capsys):
    from luna.access import Access
    _own_login(home)
    os.makedirs(home.user_token.parent, exist_ok=True)
    home.user_token.write_text('t')
    Access(args={'action': 'logout'})
    assert not home.user_ini.exists() and not home.user_token.exists()
    Access(args={'action': 'logout'})
    assert 'not logged in' in capsys.readouterr().out


# ── refusals reach the person verbatim ──────────────────────────────────────

def test_a_refusal_is_shown_as_the_daemon_worded_it(home, monkeypatch, capsys):
    from luna.access import Access
    import luna.access as access
    message = 'node node001 requires w; you hold r-x (manager in intel)'
    # the raw route helper hands the daemon's error body back as bytes; the person reads the sentence
    monkeypatch.setattr(access.Rest, 'post_raw',
                        lambda self, route, payload: types.SimpleNamespace(status_code=403, content=json.dumps({'message': message}).encode()))
    with pytest.raises(SystemExit):
        Access(args={'action': 'chmod', 'entity': 'node', 'name': 'node001', 'access': 'rwxrwx---'})
    err = capsys.readouterr().err
    assert message in err and "b'" not in err and '{' not in err, err


def test_the_three_verbs_post_to_the_generic_routes(home, monkeypatch, capsys):
    from luna.access import Access
    import luna.access as access
    posted = []
    monkeypatch.setattr(access.Rest, 'post_raw',
                        lambda self, route, payload: posted.append((route, payload)) or types.SimpleNamespace(status_code=204, content=b''))
    Access(args={'action': 'chmod', 'entity': 'otherdev', 'name': 'pdu1', 'access': '750'})
    Access(args={'action': 'chgrp', 'entity': 'node', 'name': 'node001', 'usergroups': '+intel,-amd'})
    Access(args={'action': 'chown', 'entity': 'cluster', 'name': 'cluster', 'owners': 'alice'})
    out = capsys.readouterr().out
    assert 'otherdev pdu1: access set to 750' in out and 'cluster cluster: owners set to alice' in out, \
        'a 204 carries no body: the verb says what it did'
    assert posted == [
        ('config/otherdevices/pdu1/_chmod', {'config': {'otherdevices': {'pdu1': {'access': '750'}}}}),
        ('config/node/node001/_chgrp', {'config': {'node': {'node001': {'usergroups': ['+intel', '-amd']}}}}),
        ('config/cluster/cluster/_chown', {'config': {'cluster': {'cluster': {'owners': 'alice'}}}}),
    ]


def test_every_governed_listing_shows_owners_usergroups_and_access():
    """ls -l: the three fields join every governed list and show, and no ungoverned one."""
    from luna.utils.constant import ACCESS_FIELDS, GOVERNED_TABLES, filter_columns, sortby
    for table in GOVERNED_TABLES:
        assert all(field in filter_columns(table) for field in ACCESS_FIELDS), table
        assert all(field in sortby(table) for field in ACCESS_FIELDS), table
    for table in ('user', 'usergroup', 'dns', 'groupinterface'):
        # a user's own usergroups are a listing field in their own right; owners and access are not
        assert not any(field in (filter_columns(table) or []) for field in ('owners', 'access')), table


# ── the log follows the person too ─────────────────────────────────────────

def test_the_log_falls_back_to_the_own_directory_when_the_system_log_is_not_writable(home, monkeypatch):
    """Logging in as oneself does not need root: a person who may not append to
    /var/log/luna gets a log beside their login; root keeps the system file."""
    import luna.utils.log as luna_log
    system_log = home.root / 'var' / 'luna2-cli.log'
    monkeypatch.setattr(luna_log, 'LOG_FILE', str(system_log))
    assert luna_log.Log.log_file() == str(home.root / 'home' / '.luna' / 'luna2-cli.log'), \
        'the system directory does not exist and is not ours to create'
    os.makedirs(system_log.parent)
    assert luna_log.Log.log_file() == str(system_log), 'a writable system directory wins'
    system_log.write_text('')
    os.chmod(system_log, 0o444)
    monkeypatch.setattr(os, 'access', lambda path, mode: False)
    assert luna_log.Log.log_file().endswith('.luna/luna2-cli.log'), 'a read-only system log falls back'
    assert stat.S_IMODE(os.stat(home.root / 'home' / '.luna').st_mode) == 0o700


def test_the_mode_is_shown_with_its_meaning_in_words():
    """The letters stay, because chmod takes them; every show says beside them what each
    class may do, so nobody has to know that x means operate."""
    from luna.utils.helper import Helper
    assert Helper().access_in_words('rwxr-x---') == 'rwxr-x--- (owner: read, change, operate · team: read, operate · others: nothing)'
    assert Helper().access_in_words('rw-r--r--') == 'rw-r--r-- (owner: read, change · team: read · others: read)'
    assert Helper().access_in_words(None) is None and Helper().access_in_words('770') == '770', 'anything else passes through'


def test_a_map_in_a_listing_reads_as_names_with_their_values(home):
    """luna user list showed usergroups as {} and {'physics': 'admin'}: the raw map. It reads
    as 'physics (admin)' and stays blank when empty."""
    from luna.utils.helper import Helper
    data = {'alice': {'name': 'alice', 'usergroups': {'physics': 'admin', 'chemistry': 'reader'}},
            'eve': {'name': 'eve', 'usergroups': {}}}
    fields, rows = Helper().filter_data('user', data)
    column = fields.index('usergroups')
    assert rows[0][column] == 'physics (admin), chemistry (reader)' and rows[1][column] == ''


def test_the_access_verbs_render_what_is_held_in_words(home, monkeypatch, capsys):
    """luna user access and luna usergroup access: one row per object, the three characters
    a person holds with their meaning beside them."""
    import types
    from luna.utils.helper import Helper
    from luna import user as luna_user, usergroup as luna_usergroup
    import luna.utils.rest as rest
    assert Helper().access_triplet_in_words('r-x') == 'r-x (read, operate)'
    assert Helper().access_triplet_in_words('---') == '--- (nothing)'
    answers = {'config/user/bob/_access': {'config': {'user': {'bob': {'access': {'node': {'node001': 'r--'}, 'osimage': {'shared': 'r--'}}}}}},
               'config/usergroup/intel/_access': {'config': {'usergroup': {'intel': {'access': {'node': {'node001': {'admin': 'r-x', 'manager': 'r-x', 'operator': 'r-x', 'reader': 'r--'}}}}}}}}
    monkeypatch.setattr(rest.Rest, 'get_raw', lambda self, path, **kw: types.SimpleNamespace(status_code=200, json=lambda: answers[path]))
    luna_user.User({'action': 'access', 'name': 'bob', 'raw': False, 'verbose': None})
    out = capsys.readouterr().out
    assert 'node001' in out and 'r-- (read)' in out and 'shared' in out
    luna_usergroup.UserGroup({'action': 'access', 'name': 'intel', 'raw': False, 'verbose': None})
    out = capsys.readouterr().out
    assert 'node001' in out and 'r-x (read, operate)' in out and 'r-- (read)' in out

