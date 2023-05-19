#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Secrets Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from operator import methodcaller
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log
from luna.utils.message import Message

class Secrets():
    """
    Secrets Class responsible to show, list,
    and update information for all Secrets
    """

    def __init__(self, args=None, parser=None, subparsers=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "secrets"
        if self.args:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            actions = ["list", "show", "add", "change", "clone", "remove"]
            if self.args["action"] in actions:
                call = methodcaller(f'{self.args["action"]}_secrets')
                call(self)
            else:
                Message().show_warning(f'Kindly choose from {actions}.')
        else:
            self.get_arguments(parser, subparsers)


    def get_arguments(self, parser, subparsers):
        """
        Method will provide all the arguments related to the Secrets class.
        """
        secrets_menu = subparsers.add_parser('secrets', help='Secrets operations.')
        secrets_args = secrets_menu.add_subparsers(dest='action')
        ## >>>>>>> Secrets Command >>>>>>> list
        list_secrets = secrets_args.add_parser('list', help='List Secrets')
        list_secrets.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        list_secrets.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        list_parser = list_secrets.add_subparsers(dest='entity')
        list_node = list_parser.add_parser('node', help='List Node Secrets')
        list_node.add_argument('name', help='Name of the Node')
        list_node.add_argument('-s', '--secret', help='Name of the Secret')
        list_node.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        list_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        list_group = list_parser.add_parser('group', help='List Group Secrets')
        list_group.add_argument('name', help='Name of the Group')
        list_group.add_argument('-s', '--secret', help='Name of the Secret')
        list_group.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        list_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Secrets Command >>>>>>> show
        show_secrets = secrets_args.add_parser('show', help='Show Secrets')
        show_parser = show_secrets.add_subparsers(dest='entity')
        show_node = show_parser.add_parser('node', help='Show Node Secrets')
        show_node.add_argument('name', help='Name of the Node')
        show_node.add_argument('-s', '--secret', help='Name of the Secret')
        show_node.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        show_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        show_group = show_parser.add_parser('group', help='Show Group Secrets')
        show_group.add_argument('name', help='Name of the Group')
        show_group.add_argument('secret', help='Name of the Secret')
        show_group.add_argument('-R', '--raw', action='store_true', help='Raw JSON output')
        show_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Secrets Command >>>>>>> add
        change_secrets = secrets_args.add_parser('add', help='Add A New Secret')
        change_parser = change_secrets.add_subparsers(dest='entity')
        change_node = change_parser.add_parser('node', help='Add A Node Secrets')
        change_node.add_argument('name', help='Name of the Node')
        change_node.add_argument('secret', help='Name of the Secret')
        change_node.add_argument('-c', '--content', action='store_true',
                                 help='Content of the Secret')
        change_node.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        change_node.add_argument('-p', '--path', help='Path of the Secret')
        change_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        change_group = change_parser.add_parser('group', help='Add A Group Secrets')
        change_group.add_argument('name', help='Name of the Group')
        change_group.add_argument('secret', help='Name of the Secret')
        change_group.add_argument('--content', '-c', action='store_true',
                                  help='Content of the Secret')
        change_group.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        change_group.add_argument('--path', '-p', help='Path of the Secret')
        change_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Secrets Command >>>>>>> change
        change_secrets = secrets_args.add_parser('change', help='Change Secrets')
        change_parser = change_secrets.add_subparsers(dest='entity')
        change_node = change_parser.add_parser('node', help='Change Node Secrets')
        change_node.add_argument('name', help='Name of the Node')
        change_node.add_argument('secret', help='Name of the Secret')
        change_node.add_argument('-c', '--content', action='store_true',
                                 help='Content of the Secret')
        change_node.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        change_node.add_argument('-p', '--path', help='Path of the Secret')
        change_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        change_group = change_parser.add_parser('group', help='Change Group Secrets')
        change_group.add_argument('name', help='Name of the Group')
        change_group.add_argument('secret', help='Name of the Secret')
        change_group.add_argument('--content', '-c', action='store_true',
                                  help='Content of the Secret')
        change_group.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        change_group.add_argument('--path', '-p', help='Path of the Secret')
        change_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Secrets Command >>>>>>> clone
        clone_secrets = secrets_args.add_parser('clone', help='Clone Secrets')
        clone_parser = clone_secrets.add_subparsers(dest='entity')
        clone_node = clone_parser.add_parser('node', help='Clone Node Secrets')
        clone_node.add_argument('name', help='Name of the Node')
        clone_node.add_argument('secret', help='Name of the Secret')
        clone_node.add_argument('newsecretname', help='New name for the Secret')
        clone_node.add_argument('--content', '-c', action='store_true',
                                help='Content of the Secret')
        clone_node.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        clone_node.add_argument('--path', '-p', help='Path of the Secret')
        clone_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        clone_group = clone_parser.add_parser('group', help='Clone Group Secrets')
        clone_group.add_argument('name', help='Name of the Group')
        clone_group.add_argument('secret', help='Name of the Secret')
        clone_group.add_argument('newsecretname', help='New name for the Secret')
        clone_group.add_argument('--content', '-c', action='store_true',
                                 help='Content of the Secret')
        clone_group.add_argument('-qc', '--quick-content', dest='content',
                                metavar="File-Path OR In-Line", help='Content File-Path OR In-Line')
        clone_group.add_argument('--path', '-p', help='Path of the Secret')
        clone_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        ## >>>>>>> Secrets Command >>>>>>> delete
        remove_secrets = secrets_args.add_parser('remove', help='Remove Secrets')
        remove_parser = remove_secrets.add_subparsers(dest='entity')
        remove_node = remove_parser.add_parser('node', help='Remove Node Secrets')
        remove_node.add_argument('name', help='Name of the Node')
        remove_node.add_argument('secret', help='Name of the Secret')
        remove_node.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        remove_group = remove_parser.add_parser('group', help='Remove Group Secrets')
        remove_group.add_argument('name', help='Name of the Group')
        remove_group.add_argument('secret', help='Name of the Secret')
        remove_group.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
        return parser


    def list_secrets(self):
        """
        Method to list Secrets all or only node or
        only group depending on the arguments.
        """
        error = False
        uri = self.route
        if 'name' in self.args:
            uri = f'{uri}/{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                uri = f'{uri}/{self.args["secret"]}'
        if self.args["entity"]:
            if self.args['name'] is None:
                error = Message().show_error('Kindly Choose a Node or Group.')
        if error is False:
            self.logger.debug(f'Secret URI => {uri}')
            get_list = Rest().get_data(uri)
            self.logger.debug(f'Get List Data from Helper => {get_list}')
            if get_list:
                data = get_list['config']['secrets']
                if self.args['raw']:
                    json_data = Helper().prepare_json(data)
                    Presenter().show_json(json_data)
                else:
                    if 'group' in data:
                        table = f'group{self.route}'
                        fields, rows  =  Helper().get_secrets(table, data['group'])
                        self.logger.debug(f'Fields => {fields}')
                        self.logger.debug(f'Rows => {rows}')
                        if 'name' in self.args:
                            title = f' << Group {self.args["name"]} Secrets >>'
                        else:
                            title = ' << Group Secrets >>'
                        Presenter().show_table(title, fields, rows)
                    if 'node' in data:
                        table = f'node{self.route}'
                        fields, rows  =  Helper().get_secrets(table, data['node'])
                        self.logger.debug(f'Fields => {fields}')
                        self.logger.debug(f'Rows => {rows}')
                        if 'name' in self.args:
                            title = f' << Node {self.args["name"]} Secrets >>'
                        else:
                            title = ' << Node Secrets >>'
                        Presenter().show_table(title, fields, rows)
            else:
                Message().show_error(f'{self.route} are not found.')
        return True


    def show_secrets(self):
        """
        Method to show Secrets for node or group
        or only-one depending on the arguments.
        """
        response = False
        if self.args['entity'] is not None:
            uri = f'{self.route}/{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                uri = f'{uri}/{self.args["secret"]}'
            self.logger.debug(f'Secret URI => {uri}')
            get_list = Rest().get_data(uri)
            self.logger.debug(f'Get List Data from Helper => {get_list}')
            if get_list:
                data = get_list['config']['secrets']
                if self.args['raw']:
                    json_data = Helper().prepare_json(data)
                    response = Presenter().show_json(json_data)
                else:
                    if 'group' in data:
                        table = f'group{self.route}'
                        fields, rows  = Helper().filter_secret_col(table, data['group'])
                        self.logger.debug(f'Fields => {fields}')
                        self.logger.debug(f'Rows => {rows}')
                        group_name = list(data["group"].keys())[0]
                        title = f'Group {group_name} Secrets'
                        response = Presenter().show_table_col(title, fields, rows)
                    if 'node' in data:
                        table = f'node{self.route}'
                        fields, rows  = Helper().filter_secret_col(table, data['node'])
                        self.logger.debug(f'Fields => {fields}')
                        self.logger.debug(f'Rows => {rows}')
                        title = f'Node {self.args["name"]} Secrets'
                        response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Message().show_error('Either select node or group')
        return response


    def add_secrets(self):
        """
        Method to change Secrets for node or group
        depending on the arguments.
        """
        response = False
        if self.args['entity'] is not None:
            uri = f'{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                if len(self.args["secret"]) == 1:
                    uri = f'{uri}/{self.args["secret"][0]}'
            self.logger.debug(f'Secret URI => {uri}')
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            for remove in ['verbose', 'command', 'action', 'name']:
                self.args.pop(remove, None)
            if self.args['content'] is False:
                self.args.pop('content', None)
            if self.args['path'] is None:
                self.args.pop('path', None)
            self.args['name'] = self.args['secret']
            self.args.pop('secret', None)
            pre_payload = {entity_name: [self.args], 'name': self.args['name']}
            payload = Helper().prepare_payload(None, pre_payload)
            payload.pop('name', None)
            if payload:
                request_data = {'config': {self.route: {entity: payload}}}
                self.logger.debug(f'Payload => {request_data}')
                response = Rest().post_url_data(self.route, uri, request_data)
                self.logger.debug(f'Response => {response}')
                if response.status == 201:
                    Message().show_success(f'Secret for {entity} is created.')
                else:
                    Message().error_exit(response.content, response.status)
        else:
            response = Message().show_error('Either select node or group')
        return response


    def change_secrets(self):
        """
        Method to change Secrets for node or group
        depending on the arguments.
        """
        response = False
        if self.args['entity'] is not None:
            uri = f'{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                if len(self.args["secret"]) == 1:
                    uri = f'{uri}/{self.args["secret"][0]}'
            self.logger.debug(f'Secret URI => {uri}')
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            for remove in ['verbose', 'command', 'action', 'name']:
                self.args.pop(remove, None)
            if self.args['content'] is False:
                self.args.pop('content', None)
            if self.args['path'] is None:
                self.args.pop('path', None)
            self.args['name'] = self.args['secret']
            self.args.pop('secret', None)
            pre_payload = {entity_name: [self.args], 'name': self.args['name']}
            payload = Helper().prepare_payload(f'{self.route}/{uri}', pre_payload)
            payload.pop('name', None)
            if payload:
                request_data = {'config': {self.route: {entity: payload}}}
                self.logger.debug(f'Payload => {request_data}')
                response = Rest().post_url_data(self.route, uri, request_data)
                self.logger.debug(f'Response => {response}')
                if response.status == 204:
                    Message().show_success(f'Secret for {entity} is update.')
                else:
                    Message().error_exit(response.content, response.status)
        else:
            response = Message().show_error('Either select node or group')
        return response


    def clone_secrets(self):
        """
        Method to Clone Secrets for node or group
        depending on the arguments.
        """
        response = False
        if self.args['entity'] is not None:
            uri = f'{self.args["entity"]}/{self.args["name"]}/{self.args["secret"]}'
            self.logger.debug(f'Secret URI => {uri}')
            payload = {}
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            for remove in ['verbose', 'command', 'action', 'name']:
                self.args.pop(remove, None)
            tmp_payload = self.args
            if tmp_payload['content']:
                tmp_payload['name'] = tmp_payload['newsecretname']
                content = Helper().prepare_payload(f'{self.route}/{uri}', tmp_payload)
                tmp_payload['content'] = content['content']
            tmp_payload['name'] = tmp_payload['secret']
            del tmp_payload['secret']
            payload[entity_name] = [tmp_payload]
            if payload:
                request_data = {'config': {self.route: {entity: payload}}}
                self.logger.debug(f'Payload => {request_data}')
                response = Rest().post_clone(self.route, uri, request_data)
                self.logger.debug(f'Response => {response}')
                if response.status == 204:
                    Message().show_success('Secret is Cloned.')
                else:
                    Message().error_exit(response.content, response.status)
        else:
            response = Message().show_error('Either select node or group')
        return response


    def remove_secrets(self):
        """
        Method to remove a Secrets for node or group
        depending on the arguments.
        """
        response = False
        abort = False
        if self.args['entity'] is not None:
            payload = {}
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            del self.args['name']
            if entity and self.args['secret']:
                payload['name'] = entity
                payload['secret'] = self.args['secret']
                uri = f'{entity}/{entity_name}/{payload["secret"]}'
                self.logger.debug(f'Delete URI => {uri}')
            else:
                abort = Message().show_error('Provide Node/Group name and the secret name')
            if abort is False:
                response = Rest().get_delete(self.route, uri)
                self.logger.debug(f'Response => {response}')
                if response.status == 204:
                    Message().show_success('Secret is Deleted.')
                else:
                    Message().error_exit(response.content, response.status)
        else:
            response = Message().show_error('Either select node or group')
        return response
