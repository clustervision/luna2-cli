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
Profile Class handles all profile related operations.

A profile bundles configuration files with a service to act on, and is assigned to
groups and nodes. Profiles stack: a node applies the profiles of its group plus its
own. File contents travel base64, exactly like secrets.
"""

__author__      = 'Antoine Schonewille'
__copyright__   = 'Copyright 2025, Luna2 Project'
__license__     = 'GPL'
__version__     = '2.2'
__maintainer__  = 'Antoine Schonewille'
__email__       = 'antoine.schonewille@clustervision.com'
__status__      = 'Development'

import os
from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.message import Message
from luna.utils.constant import actions, BOOL_CHOICES, BOOL_META

ACTION_CHOICES = ['restart', 'stop', 'reload', 'start', 'none']
SCOPE_CHOICES = ['static', 'dynamic']


class Profile():
    """
    Profile Class responsible to show, list, add, change,
    clone and remove information for all Profiles.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "profiles"
        self.table = "profile"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_profile')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Profile class.
        """
        profile_menu = Helper().get_help_message(subparsers, self.table)
        profile_args = profile_menu.add_subparsers(dest='action', title='commands',
                                                   description='Available profile operations')
        ## >>>>>>> Profile Command >>>>>>> list
        profile_list = profile_args.add_parser('list', help='List Profiles')
        profile_list.add_argument('-R', '--raw', action='store_true', default=None,
                                  help='Raw JSON output')
        profile_list.add_argument('-v', '--verbose', action='store_true', default=None,
                                  help='Verbose Mode')
        ## >>>>>>> Profile Command >>>>>>> show
        profile_show = profile_args.add_parser('show', help='Show a Profile')
        profile_show.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_show.add_argument('-R', '--raw', action='store_true', default=None,
                                  help='Raw JSON output')
        profile_show.add_argument('-v', '--verbose', action='store_true', default=None,
                                  help='Verbose Mode')
        ## >>>>>>> Profile Command >>>>>>> add
        profile_add = profile_args.add_parser('add', help='Add a Profile')
        profile_add.add_argument('name', help='Name of the Profile')
        self.common_profile_args(profile_add)
        ## >>>>>>> Profile Command >>>>>>> change
        profile_change = profile_args.add_parser('change', help='Change a Profile')
        profile_change.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        self.common_profile_args(profile_change)
        ## >>>>>>> Profile Command >>>>>>> clone
        profile_clone = profile_args.add_parser('clone', help='Clone a Profile including its files')
        profile_clone.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_clone.add_argument('newprofilename', help='New Name for the Profile')
        profile_clone.add_argument('-v', '--verbose', action='store_true', default=None,
                                   help='Verbose Mode')
        profile_rename = profile_args.add_parser('rename', help='Rename a Profile')
        profile_rename.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_rename.add_argument('newprofilename', help='New Name for the Profile')
        profile_rename.add_argument('-v', '--verbose', action='store_true', default=None,
                                    help='Verbose Mode')
        ## >>>>>>> Profile Command >>>>>>> remove
        profile_remove = profile_args.add_parser('remove', help='Remove a Profile and its files')
        profile_remove.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_remove.add_argument('-v', '--verbose', action='store_true', default=None,
                                    help='Verbose Mode')
        ## >>>>>>> Profile Command >>>>>>> status
        profile_status = profile_args.add_parser('status', help='Where every node stands')
        profile_status.add_argument('name', nargs='?', help='Name of a single Node').completer = Helper().name_completer("node")
        profile_status.add_argument('-a', '--all', action='store_true', default=None,
                                    help='List every node, not only the ones needing attention')
        profile_status.add_argument('-R', '--raw', action='store_true', default=None,
                                    help='Raw JSON output')
        profile_status.add_argument('-v', '--verbose', action='store_true', default=None,
                                    help='Verbose Mode')
        ## >>>>>>> Profile Command >>>>>>> addfile
        profile_addfile = profile_args.add_parser('addfile', help='Add a file to a Profile')
        profile_addfile.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_addfile.add_argument('file', help='Name of the file inside the Profile')
        self.common_file_args(profile_addfile)
        ## >>>>>>> Profile Command >>>>>>> changefile
        profile_changefile = profile_args.add_parser('changefile', help='Change a file in a Profile')
        profile_changefile.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_changefile.add_argument('file', help='Name of the file inside the Profile')
        self.common_file_args(profile_changefile)
        ## >>>>>>> Profile Command >>>>>>> removefile
        profile_removefile = profile_args.add_parser('removefile', help="Remove one file from a Profile")
        profile_removefile.add_argument('name', help='Name of the Profile').completer = Helper().name_completer(self.route)
        profile_removefile.add_argument('file', help='Name of the file inside the Profile')
        profile_removefile.add_argument('-v', '--verbose', action='store_true', default=None,
                                        help='Verbose Mode')
        return parser


    def common_profile_args(self, parser):
        """
        The arguments shared by add and change. The files are not here: a profile holds
        several of them and an editor edits one thing at a time, so they have verbs of
        their own - addfile, changefile, removefile - exactly as a secret does.
        """
        parser.add_argument('-S', '--scope', choices=SCOPE_CHOICES,
                            help='Scope of the Profile. Static is applied at install time')
        parser.add_argument('-s', '--service', help='Service on the node this Profile acts on')
        # dest is deliberately not 'action': the subparsers use that name for the
        # command itself, and a collision makes every profile command dispatch to
        # the service action instead
        parser.add_argument('-a', '--action', choices=ACTION_CHOICES, dest='service_action',
                            help='What to do with the service on the node')
        parser.add_argument('-e', '--enabled', choices=BOOL_CHOICES, metavar=BOOL_META,
                            help='A disabled Profile is left alone on the nodes that have '
                                 'it; only removing it from them puts anything back')
        parser.add_argument('-v', '--verbose', action='store_true', default=None,
                            help='Verbose Mode')


    def common_file_args(self, parser):
        """The arguments shared by addfile and changefile."""
        parser.add_argument('-p', '--path', help='Where the file goes on the node')
        parser.add_argument('-c', '--content', action='store_true',
                            help='Content of the file, in an editor')
        parser.add_argument('-qc', '--quick-content', dest='content',
                            metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        parser.add_argument('-o', '--owner', help='Owner of the file: user or user:group, '
                                                  'names or numeric ids')
        parser.add_argument('-m', '--mode', help='Permissions of the file, as octal digits '
                                                 '(default 644)')
        parser.add_argument('-v', '--verbose', action='store_true', default=None,
                            help='Verbose Mode')


    def file_content(self, source):
        """
        Content of a profile file, base64 encoded: read from the path when the
        argument names an existing file, taken literally otherwise. Same rule the
        rest of the CLI applies to a content argument.
        """
        if os.path.exists(source):
            if not os.path.isfile(source):
                Message().error_exit(f'ERROR :: {source} is a Invalid filepath.')
            with open(source, 'rb') as file_data:
                return Helper().base64_encode(file_data.read())
        return Helper().base64_encode(bytes(source, 'utf-8'))


    def profile_payload(self):
        """The request body for a profile, with the CLI-only arguments stripped out."""
        payload = {}
        for field in ['scope', 'service']:
            if self.args.get(field) is not None:
                payload[field] = self.args[field]
        if self.args.get('service_action') is not None:
            payload['action'] = self.args['service_action']
        # 'enabled' is converted on its own rather than by running the payload through
        # choice_to_bool: 'service' is in BOOL_KEYS because it is a yes/no on a NODE, and
        # a profile's service is the name of a unit - that helper would turn 'cron' into
        # False, and it did
        enabled = self.args.get('enabled')
        if enabled is not None:
            payload['enabled'] = '' if enabled == '' else \
                str(enabled).lower() in ['y', 'yes', 'true']
        return payload


    def list_profile(self):
        """
        Method to list all Profiles.
        """
        get_list = Rest().get_data(self.route)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if not get_list:
            return Message().show_error('Profiles are not found.')
        data = get_list['config']['profiles']
        if self.args['raw']:
            return Presenter().show_json(Helper().prepare_json(data))
        rows, fields = [], ['#', 'name', 'scope', 'service', 'action', 'files']
        num = 1
        for name, detail in data.items():
            rows.append([
                num, name, detail.get('scope'), detail.get('service'),
                detail.get('action'),
                ', '.join(entry['name'] for entry in detail.get('files') or []),
            ])
            num = num + 1
        return Presenter().show_table(' << Profiles >>', fields, rows)


    def show_profile(self):
        """
        Method to show a Profile including its files.
        """
        uri = f'{self.route}/{self.args["name"]}'
        get_list = Rest().get_data(uri)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        self.logger.debug(f'Get List Data from Helper => {get_list}')
        if not get_list:
            return Message().show_error(f'Profile {self.args["name"]} is not found.')
        detail = get_list['config']['profiles'][self.args['name']]
        if self.args['raw']:
            return Presenter().show_json(Helper().prepare_json(detail))
        fields = ['name', 'scope', 'service', 'action']
        rows = [self.args['name'], detail.get('scope'), detail.get('service'),
                detail.get('action')]
        for entry in detail.get('files') or []:
            content = Helper().base64_decode(entry.get('content'))
            if content is not None and len(content) > 60:
                content = content[:60] + '...'
            fields.append(f'file {entry["name"]}')
            rows.append(
                f'path: {entry.get("path")}\nowner: {entry.get("owner")}\n'
                f'mode: {entry.get("mode")}\ncontent: {content}'
            )
        return Presenter().show_table_col(f'Profile {self.args["name"]}', fields, rows)


    def add_profile(self):
        """
        Method to add a Profile.
        """
        name = self.args['name']
        existing = Rest().get_data(f'{self.route}/{name}')
        if existing.status_code == 200:
            Message().error_exit(f'Profile {name} already present', existing.status_code)
        payload = self.profile_payload()
        if not payload:
            return Message().show_error('Nothing to add: supply a service, an action or a file')
        request_data = {'config': {self.route: {name: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code in (200, 201, 204):
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def change_profile(self):
        """
        Method to change a Profile. Files are matched by name: the ones supplied are
        created or updated, the ones left out stay as they are. Use removefile to
        take one away.
        """
        name = self.args['name']
        existing = Rest().get_data(f'{self.route}/{name}')
        if existing.status_code != 200:
            Message().error_exit(f'Kindly add the profile {name} first', existing.status_code)
        payload = self.profile_payload()
        if not payload:
            return Message().show_error('Nothing to change: supply a service, an action or a file')
        request_data = {'config': {self.route: {name: payload}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code in (200, 201, 204):
            Message().show_success(f'Profile {name} is updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def rename_profile(self):
        """
        Method to rename a Profile. Everything that applies it keeps applying it: an
        assignment holds the profile's reference, not the name being changed here.
        """
        name = self.args['name']
        request_data = {'config': {self.route: {name: {
            'newprofilename': self.args['newprofilename']}}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code in (200, 201, 204):
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def clone_profile(self):
        """
        Method to clone a Profile including its files.
        """
        name = self.args['name']
        request_data = {'config': {self.route: {name: {
            'newprofilename': self.args['newprofilename']}}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_clone(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        if response.status_code in (200, 201, 204):
            Message().show_success(response.content)
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def remove_profile(self):
        """
        Method to remove a Profile and its files.
        """
        name = self.args['name']
        response = Rest().get_delete(self.route, name)
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'Profile {name} is removed.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def file_payload(self, existing=None):
        """
        The body for one file. The editor path is handled here rather than through
        prepare_payload: that helper pulls the current value with a nested lookup and
        takes the first match, which is the wrong file as soon as a profile holds more
        than one.
        """
        payload = {'name': self.args['file']}
        for field in ['path', 'owner', 'mode']:
            if self.args.get(field) is not None:
                payload[field] = self.args[field]
        content = self.args.get('content')
        if content is True:
            payload['content'] = Helper().open_editor(
                'content', (existing or {}).get('content'), {'name': self.args['file']})
        elif content:
            payload['content'] = self.file_content(content)
        return payload


    def profile_file(self, name=None, filename=None):
        """One file of a profile as it stands, or None."""
        get_list = Rest().get_data(f'{self.route}/{name}')
        if get_list.status_code != 200:
            return None
        detail = get_list.content['config']['profiles'].get(name) or {}
        for entry in detail.get('files') or []:
            if entry.get('name') == filename:
                return entry
        return None


    def post_file(self, payload):
        """Send one file to the profile it belongs to."""
        name = self.args['name']
        request_data = {'config': {self.route: {name: {'files': [payload]}}}}
        self.logger.debug(f'Payload => {request_data}')
        response = Rest().post_data(self.route, name, request_data)
        self.logger.debug(f'Response => {response}')
        return response


    def status_profile(self):
        """
        Method to show where every node stands with its profiles.
        """
        uri = f'{self.route}/status'
        if self.args.get('name'):
            uri = f'{uri}/{self.args["name"]}'
        get_list = Rest().get_data(uri)
        if get_list.status_code == 200:
            get_list = get_list.content
        else:
            Message().error_exit(get_list.content, get_list.status_code)
        if not get_list:
            return Message().show_error('No profile status available.')
        data = get_list['config']['profiles']['status']
        summary = get_list['config']['profiles'].get('summary') or {}
        if self.args['raw']:
            return Presenter().show_json(Helper().prepare_json(get_list['config']['profiles']))

        # a healthy node says nothing an operator needs to act on, and on a cluster of
        # any size listing them all buries the handful that do. The counts answer 'is it
        # fine'; the rows are only what is not.
        if not self.args.get('name'):
            counts = [[state, summary[state]] for state in sorted(summary)]
            Presenter().show_table(' << Profile Status >>', ['state', 'nodes'], counts)

        show_all = self.args.get('all') or self.args.get('name')
        if show_all:
            fields = ['#', 'node', 'profiles', 'state', 'frozen', 'detail', 'since']
            rows, num = [], 1
            for node in sorted(data):
                entry = data[node]
                detail = entry.get('detail') or ''
                if len(detail) > 40:
                    detail = detail[:40] + '...'
                rows.append([num, node, entry.get('profiles') or '-', entry.get('state'),
                             entry.get('frozen') or '-', detail or '-',
                             entry.get('since') or '-'])
                num = num + 1
            return Presenter().show_table(' << Profile Status >>', fields, rows)

        # failures on a cluster share a cause: a switch, a subnet, an image without
        # python. One line per cause with a count and a few names is what an operator
        # can act on; two hundred rows saying the same thing is what they scroll past.
        causes = {}
        for node in sorted(data):
            entry = data[node]
            if entry.get('state') not in ('failed', 'given up'):
                continue
            reason = (entry.get('detail') or 'unknown').split(chr(10))[0]
            reason = reason.replace(node, '<node>')
            if entry.get('state') == 'given up':
                # a node nobody is chasing any more looks exactly like one that is still
                # being retried, and that is the difference an operator has to act on
                reason = f'[not retrying] {reason}'
            causes.setdefault(reason, []).append(node)
        if causes:
            fields = ['#', 'nodes', 'reason', 'for example']
            rows, num = [], 1
            for reason in sorted(causes, key=lambda key: -len(causes[key])):
                nodes = causes[reason]
                shown = ', '.join(nodes[:3]) + (' ...' if len(nodes) > 3 else '')
                rows.append([num, len(nodes),
                             reason[:60] + ('...' if len(reason) > 60 else ''), shown])
                num = num + 1
            Presenter().show_table(' << Failing, by cause >>', fields, rows)

        stopped = sorted(node for node, entry in data.items()
                         if entry.get('state') == 'given up')
        if stopped:
            shown = ', '.join(stopped[:6]) + (' ...' if len(stopped) > 6 else '')
            Message().show_warning(f'{len(stopped)} node(s) have been failing for over a '
                                   f'day and are no longer being retried: {shown}. '
                                   f'Changing a profile they carry starts them over.')
        frozen = sorted(node for node, entry in data.items()
                        if entry.get('state') == 'frozen')
        if frozen:
            shown = ', '.join(frozen[:6]) + (' ...' if len(frozen) > 6 else '')
            Message().show_warning(f'{len(frozen)} node(s) carry a frozen profile, whose '
                                   f'files are no longer managed: {shown}')
        behind = sorted(node for node, entry in data.items()
                        if entry.get('state') == 'behind')
        if behind:
            # not an error - they are queued or in flight - but claiming that nothing
            # needs attention while a third of the cluster is waiting would be a lie
            shown = ', '.join(behind[:6]) + (' ...' if len(behind) > 6 else '')
            Message().show_warning(f'{len(behind)} node(s) are behind and waiting for '
                                   f'delivery: {shown}')
        if not causes and not frozen and not behind:
            Message().show_success('Every node has the profiles it should.')
        return True


    def addfile_profile(self):
        """
        Method to add a file to a Profile.
        """
        name, filename = self.args['name'], self.args['file']
        if Rest().get_data(f'{self.route}/{name}').status_code != 200:
            Message().error_exit(f'Profile {name} is not available', 404)
        if self.profile_file(name, filename):
            Message().error_exit(f'File {filename} is already in profile {name}', 400)
        payload = self.file_payload()
        for required in ['path', 'content']:
            if not payload.get(required):
                return Message().show_error(f'A file needs a {required}: '
                                            f'supply -p and -c or -qc')
        response = self.post_file(payload)
        if response.status_code in (200, 201, 204):
            Message().show_success(f'File {filename} is added to profile {name}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def changefile_profile(self):
        """
        Method to change a file in a Profile. What is not supplied keeps the value it
        already has, so the editor opens on the content that is actually stored.
        """
        name, filename = self.args['name'], self.args['file']
        existing = self.profile_file(name, filename)
        if not existing:
            Message().error_exit(f'File {filename} is not in profile {name}. '
                                 f'Use addfile to create it', 404)
        payload = self.file_payload(existing)
        if list(payload.keys()) == ['name']:
            return Message().show_error('Nothing to change: supply a path, content, '
                                        'owner or mode')
        response = self.post_file(payload)
        if response.status_code in (200, 201, 204):
            Message().show_success(f'File {filename} in profile {name} is updated.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response


    def removefile_profile(self):
        """
        Method to remove one file from a Profile.
        """
        name, filename = self.args['name'], self.args['file']
        response = Rest().get_delete(self.route, f'{name}/{filename}')
        self.logger.debug(f'Response => {response}')
        if response.status_code == 204:
            Message().show_success(f'File {filename} is removed from profile {name}.')
        else:
            Message().error_exit(response.content, response.status_code)
        return response
