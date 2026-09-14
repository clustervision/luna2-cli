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
Two things an operator met on a live cluster, both in what the CLI renders or sends
rather than in what the daemon answers:

  (1) `luna secrets show node <n>` and `luna secrets list` rendered the group and node
      sections and left the cluster section out. The daemon's answer carried it and the
      installer writes it, so the operator was shown two scopes of the three. The
      sections are now derived from what the daemon answered, so a scope cannot be
      forgotten by the renderer again.
  (2) `luna profile addfile` refused a profile that did not exist, and `luna profile add`
      cannot carry a file - so a profile that only places files could not be created
      without inventing a service for it. The first file now creates the profile.

The logger is stubbed rather than initialised, and Rest is faked at the module the code
imports it into, as the other files here do.
"""
import logging

import pytest

import luna.utils.log as luna_log


@pytest.fixture(autouse=True)
def _stub_logger():
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


class FakeResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


def _secret(name, path):
    return {'name': name, 'path': path, 'content': 'c2VjcmV0',
            'owner': 'root:root', 'mode': '600', 'resolved_owner': '0:0'}


# what the daemon answers for a node that has all three scopes - the shape of
# GET /config/secrets/node/<name>, which is also what the installer reads
NODE_VIEW = {'config': {'secrets': {
    'cluster': [_secret('munge-key', '/etc/munge/munge.key')],
    'group': {'compute': [_secret('nfs-keytab', '/etc/krb5.keytab')]},
    'node': {'node003': [_secret('host-key', '/etc/pki/tls/private/node.key')]},
}}}


class Recorder:
    """A Presenter that remembers the titles it was asked to render, in order."""
    titles = []

    def show_table(self, title=None, fields=None, rows=None):
        Recorder.titles.append(title)
        return True

    def show_table_col(self, title=None, field=None, rows=None, divider=None):
        Recorder.titles.append(title)
        return True


def _secrets(monkeypatch, args, answer):
    from luna.secrets import Secrets
    monkeypatch.setattr('luna.secrets.Rest', lambda: type('R', (), {
        'get_data': lambda self, uri: FakeResponse(answer)})())
    monkeypatch.setattr('luna.secrets.Presenter', Recorder)
    Recorder.titles = []
    secrets = Secrets.__new__(Secrets)
    secrets.route = 'secrets'
    secrets.logger = logging.getLogger('luna2-cli-tests')
    secrets.args = args
    return secrets


def _scopes_in(answer):
    return list(answer['config']['secrets'])


def test_show_node_renders_every_scope_the_daemon_answered(monkeypatch):
    secrets = _secrets(monkeypatch, {'entity': 'node', 'name': 'node003', 'secret': None,
                                     'raw': None}, NODE_VIEW)
    secrets.show_secrets()
    for scope in _scopes_in(NODE_VIEW):
        assert any(scope.capitalize() in title for title in Recorder.titles), \
            f'the {scope} section was not rendered: {Recorder.titles}'
    assert Recorder.titles[0] == 'Cluster Secrets', \
        'the cluster section comes first, as the installer applies it first'
    assert 'Group compute Secrets' in Recorder.titles
    assert 'Node node003 Secrets' in Recorder.titles


def test_list_everything_renders_every_scope_the_daemon_answered(monkeypatch):
    secrets = _secrets(monkeypatch, {'entity': None, 'secret': None, 'raw': None}, NODE_VIEW)
    secrets.list_secrets()
    for scope in _scopes_in(NODE_VIEW):
        assert any(scope.capitalize() in title for title in Recorder.titles), \
            f'the {scope} section was not rendered: {Recorder.titles}'
    assert Recorder.titles[0] == ' << Cluster Secrets >>'


def test_a_nodes_list_heads_the_group_section_with_the_group(monkeypatch):
    """A node's list carries its group's secrets; they were headed with the node's name."""
    secrets = _secrets(monkeypatch, {'entity': 'node', 'name': 'node003', 'secret': None,
                                     'raw': None}, NODE_VIEW)
    secrets.list_secrets()
    assert ' << Group compute Secrets >>' in Recorder.titles, Recorder.titles
    assert ' << Node node003 Secrets >>' in Recorder.titles, Recorder.titles


class Messages:
    """A Message that records instead of printing, and never exits."""
    said = []

    def show_success(self, message=None):
        Messages.said.append(('success', message))
        return True

    def show_error(self, message=None, code=None):
        Messages.said.append(('error', message))
        return False

    def error_exit(self, message=None, code=None):
        Messages.said.append(('exit', message))
        raise SystemExit(code)


def _profile(monkeypatch, args, exists):
    from luna.profile import Profile
    posted = []

    class FakeRest:
        def get_data(self, uri):
            if exists:
                return FakeResponse({'config': {'profiles': {'banner': {'files': []}}}})
            return FakeResponse({'message': 'Profile banner is not available'}, 404)

        def post_data(self, route, name, data):
            posted.append((route, name, data))
            return FakeResponse('created', 201)

    monkeypatch.setattr('luna.profile.Rest', FakeRest)
    monkeypatch.setattr('luna.profile.Message', Messages)
    Messages.said = []
    profile = Profile.__new__(Profile)
    profile.route = 'profiles'
    profile.logger = logging.getLogger('luna2-cli-tests')
    profile.args = args
    return profile, posted


ADDFILE = {'name': 'banner', 'file': 'motd', 'path': '/etc/motd', 'content': 'hello',
           'owner': None, 'mode': None}


def test_addfile_creates_a_profile_that_does_not_exist_yet(monkeypatch):
    profile, posted = _profile(monkeypatch, dict(ADDFILE), exists=False)
    profile.addfile_profile()
    assert posted, 'nothing was sent: the file-only profile was refused'
    route, name, data = posted[0]
    assert (route, name) == ('profiles', 'banner')
    assert data['config']['profiles']['banner']['files'][0]['path'] == '/etc/motd'
    assert Messages.said == [('success', 'Profile banner created with file motd.')]


def test_addfile_on_an_existing_profile_still_adds_to_it(monkeypatch):
    profile, posted = _profile(monkeypatch, dict(ADDFILE), exists=True)
    profile.addfile_profile()
    assert posted
    assert Messages.said == [('success', 'File motd is added to profile banner.')]


def test_addfile_still_needs_a_path_and_content(monkeypatch):
    args = dict(ADDFILE, path=None)
    profile, posted = _profile(monkeypatch, args, exists=False)
    profile.addfile_profile()
    assert not posted
    assert Messages.said and Messages.said[0][0] == 'error'
