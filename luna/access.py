#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
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
Access Class for the CLI: logging in as oneself, asking who one is, and changing who
may do what with an object, as chmod, chgrp and chown do for a file.
"""
__author__      = "Antoine Schonewille"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Antoine Schonewille"
__email__       = "antoine.schonewille@clustervision.com"
__status__      = "Development"

import json
import os
from configparser import RawConfigParser
from getpass import getpass
from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.log import Log
from luna.utils.rest import Rest
from luna.utils.constant import actions, INI_FILE, USER_INI_FILE, USER_TOKEN_FILE
from luna.utils.message import Message
from luna.utils.presenter import Presenter

# Every governed entity, as the CLI names it, and as the daemon names it.
GOVERNED = {'node': 'node', 'group': 'group', 'osimage': 'osimage', 'bmcsetup': 'bmcsetup',
            'redfishsetup': 'redfishsetup', 'biosconfig': 'biosconfig', 'firmwarecatalog': 'firmwarecatalog',
            'profile': 'profile', 'cluster': 'cluster', 'network': 'network', 'route': 'route',
            'cloud': 'cloud', 'switch': 'switch', 'rack': 'rack', 'otherdev': 'otherdevices'}


def _message(response):
    """
    The daemon's own sentence out of an error answer, so a refusal reads as the daemon
    worded it and not as a JSON body.
    """
    content = response.content
    try:
        body = json.loads(content) if isinstance(content, (bytes, str)) else content
        return body.get('message', content) if isinstance(body, dict) else content
    except ValueError:
        return content.decode() if isinstance(content, bytes) else content


class Access():
    """
    Access Class responsible for login, logout, whoami, chmod, chgrp and chown.
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.table = "access"
        self.actions = actions(self.table)
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] in self.actions:
                call = methodcaller(f'{self.args["action"]}_access')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {self.actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Access class.
        """
        menu = Helper().get_help_message(subparsers, self.table)
        args = menu.add_subparsers(dest='action', title='commands', description='Available access operations')
        login = args.add_parser('login', help='Log in as yourself: writes ~/.luna/luna.ini and fetches a token')
        login.add_argument('username', nargs='?', help='Username (asked when omitted)')
        login.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        logout = args.add_parser('logout', help='Forget your login: removes ~/.luna/luna.ini and the token')
        logout.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        whoami = args.add_parser('whoami', help='Who the daemon takes you for, and your usergroups with roles')
        whoami.add_argument('-R', '--raw', action='store_true', default=None, help='Raw JSON output')
        whoami.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        for verb, field, text in (('chmod', 'access', 'The mode as ls shows it (rwxr-x---) or octal (750)'),
                                  ('chgrp', 'usergroups', 'Usergroups: a list to replace, +name to add, -name to remove'),
                                  ('chown', 'owners', 'Owners: a list to replace, +name to add, -name to remove')):
            sub = args.add_parser(verb, help=f'Change the {field} of an object')
            sub.add_argument('entity', choices=sorted(GOVERNED), help='What kind of object')
            sub.add_argument('name', help='Its name (cluster for the cluster)')
            sub.add_argument(field, help=text)
            sub.add_argument('-v', '--verbose', action='store_true', default=None, help='Verbose Mode')
        return parser


    def login_access(self):
        """
        Write the person's own credential file and fetch a token into their own cache.
        Root without a username keeps the controller's account rather than shadowing it.
        """
        username = self.args.get('username')
        if not username:
            if os.geteuid() == 0:
                Message().error_exit('root already holds the controller account; give a username to log in as somebody else')
            username = input('Username: ')
        password = getpass('Password: ')
        endpoint, protocol, verify = self._controller_endpoint()
        ini_path = os.path.expanduser(USER_INI_FILE)
        os.makedirs(os.path.dirname(ini_path), mode=0o700, exist_ok=True)
        parser = RawConfigParser()
        parser['API'] = {'USERNAME': username, 'PASSWORD': password, 'ENDPOINT': endpoint,
                         'PROTOCOL': protocol, 'VERIFY_CERTIFICATE': verify}
        with open(ini_path, 'w', encoding='utf-8') as handle:
            parser.write(handle)
        os.chmod(ini_path, 0o600)
        token_path = os.path.expanduser(USER_TOKEN_FILE)
        if os.path.exists(token_path):
            os.remove(token_path)
        rest = Rest()
        if rest.ini_file != ini_path:
            Message().error_exit(f'{ini_path} was written but is not the file in use')
        rest.token()
        Message().show_success(f'Logged in as {username}; credentials in {ini_path}, token in {token_path}.')


    def _controller_endpoint(self):
        """
        The daemon's address from the controller ini when readable, so a person need not know it.
        """
        parser = RawConfigParser()
        if os.path.isfile(INI_FILE) and os.access(INI_FILE, os.R_OK):
            parser.read(INI_FILE)
        if parser.has_section('API'):
            return (parser.get('API', 'ENDPOINT', fallback='localhost:7050'),
                    parser.get('API', 'PROTOCOL', fallback='https'),
                    parser.get('API', 'VERIFY_CERTIFICATE', fallback='no'))
        return input('Daemon endpoint (host:port): '), 'https', 'no'


    def logout_access(self):
        """
        Remove the person's own credential file and token cache.
        """
        removed = []
        for path in (USER_INI_FILE, USER_TOKEN_FILE):
            full = os.path.expanduser(path)
            if os.path.exists(full):
                os.remove(full)
                removed.append(full)
        Message().show_success('Removed ' + ', '.join(removed) if removed else 'Nothing to remove: you were not logged in.')


    def whoami_access(self):
        """
        GET /whoami.
        """
        response = Rest().get_raw('whoami')
        if response.status_code != 200:
            Message().error_exit(_message(response), response.status_code)
        answer = response.json()
        if self.args.get('raw'):
            return Presenter().show_json(answer)
        rows = [['user', answer['user']], ['id', answer['id']], ['source', answer['source']],
                ['admin', 'yes' if answer['admin'] else 'no'],
                ['usergroups', ', '.join(f'{g} ({r})' for g, r in sorted(answer['usergroups'].items())) or '-'],
                ['hardware', ', '.join(answer.get('hardware') or []) or '-']]
        return Presenter().show_table('whoami', ['field', 'value'], rows)


    def _change(self, verb, field):
        """
        The three verbs differ only in the field they carry.
        """
        entity = GOVERNED[self.args['entity']]
        name = self.args['name']
        value = self.args[field]
        if field != 'access' and ',' in value:
            value = [item.strip() for item in value.split(',')]
        body = {'config': {entity: {name: {field: value}}}}
        response = Rest().post_raw(f'config/{entity}/{name}/_{verb}', body)
        if response.status_code in (201, 204):
            # an update answers 204 with no body, as every update does: say what was done
            Message().show_success(f'{self.args["entity"]} {name}: {field} set to {self.args[field]}.')
        else:
            Message().error_exit(_message(response), response.status_code)

    def chmod_access(self):
        return self._change('chmod', 'access')

    def chgrp_access(self):
        return self._change('chgrp', 'usergroups')

    def chown_access(self):
        return self._change('chown', 'owners')
