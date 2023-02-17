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
__status__      = "Production"


from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.inquiry import Inquiry
from luna.utils.rest import Rest

"""
Secrets Commands:

program = luna
parser = secrets
parser = list, show, update, delete, clone
parser = node, group
arguments = -R, -s

1. luna secrets list -R
2. luna secrets list node node001 -R
3. luna secrets list group compute -R
4. luna secrets list node node001 -s license -R
5. luna secrets list group compute -s sshkey -R

7. luna secrets show node node001 -R
8. luna secrets show group compute -R
9. luna secrets show node node001 -s license -R
10. luna secrets show group compute -s sshkey -R

11. luna secrets update node node001 append(-s secretname -c content -p path)
12. luna secrets update group compute append(-s secretname -c content -p path)

13. luna secrets delete node node001 -s secretname
14. luna secrets delete group compute -s secretname

13. luna secrets clone node node001 -s secretname -ns newsecretname -c content -p path
14. luna secrets clone group compute -s secretname -ns newsecretname -c content -p path



"""
class Secrets(object):
    """
    Secrets Class responsible to show, list,
    and update information for all Secrets
    """

    def __init__(self, args=None):
        self.args = args
        self.route = "secrets"
        if self.args:
            if self.args["action"] == "list":
                self.list_secrets()
            elif self.args["action"] == "show":
                self.show_secrets()
            elif self.args["action"] == "update":
                self.update_secrets()
            elif self.args["action"] == "clone":
                self.clone_secrets()
            elif self.args["action"] == "delete":
                self.delete_secrets()
            else:
                print("Not a valid option.")
        else:
            print("Please pass -h to see help menu.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Secrets class.
        """
        secrets_menu = subparsers.add_parser('secrets', help='Secrets operations.')
        secrets_args = secrets_menu.add_subparsers(dest='action')
        ## >>>>>>> Secrets Command >>>>>>> list
        list_secrets = secrets_args.add_parser('list', help='List Secrets')
        list_secrets.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        list_parser = list_secrets.add_subparsers(dest='entity')
        list_node = list_parser.add_parser('node', help='List Node Secrets')
        list_node.add_argument('name', help='Name of the Node')
        list_node.add_argument('--secret', '-s', help='Name of the Secret')
        list_node.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        list_group = list_parser.add_parser('group', help='List Group Secrets')
        list_group.add_argument('name', help='Name of the Group')
        list_group.add_argument('--secret', '-s', help='Name of the Secret')
        list_group.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Secrets Command >>>>>>> show
        show_secrets = secrets_args.add_parser('show', help='Show Secrets')
        show_parser = show_secrets.add_subparsers(dest='entity')
        show_node = show_parser.add_parser('node', help='Show Node Secrets')
        show_node.add_argument('name', help='Name of the Node')
        show_node.add_argument('--secret', '-s', help='Name of the Secret')
        show_node.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        show_group = show_parser.add_parser('group', help='Show Group Secrets')
        show_group.add_argument('name', help='Name of the Group')
        show_group.add_argument('--secret', '-s', help='Name of the Secret')
        show_group.add_argument('--raw', '-R', action='store_true', help='Raw JSON output')
        ## >>>>>>> Secrets Command >>>>>>> update
        update_secrets = secrets_args.add_parser('update', help='Update Secrets')
        update_parser = update_secrets.add_subparsers(dest='entity')
        update_node = update_parser.add_parser('node', help='Update Node Secrets')
        update_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        update_node.add_argument('--name', '-n', help='Name of the Node')
        update_node.add_argument('--secret', '-s', action='append', help='Name of the Secret')
        update_node.add_argument('--content', '-c', action='append', help='Content of the Secret')
        update_node.add_argument('--path', '-p', action='append', help='Path of the Secret')
        update_group = update_parser.add_parser('group', help='Update Group Secrets')
        update_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        update_group.add_argument('--name', '-n', help='Name of the Group')
        update_group.add_argument('--secret', '-s', action='append', help='Name of the Secret')
        update_group.add_argument('--content', '-c', action='append', help='Content of the Secret')
        update_group.add_argument('--path', '-p', action='append', help='Path of the Secret')
        ## >>>>>>> Secrets Command >>>>>>> clone
        clone_secrets = secrets_args.add_parser('clone', help='Clone Secrets')
        clone_parser = clone_secrets.add_subparsers(dest='entity')
        clone_node = clone_parser.add_parser('node', help='Clone Node Secrets')
        clone_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        clone_node.add_argument('--name', '-n', help='Name of the Node')
        clone_node.add_argument('--secret', '-s', help='Name of the Secret')
        clone_node.add_argument('--newsecretname', '-nn', help='New name for the Secret')
        clone_node.add_argument('--content', '-c', help='Content of the Secret')
        clone_node.add_argument('--path', '-p', help='Path of the Secret')
        clone_group = clone_parser.add_parser('group', help='Clone Group Secrets')
        clone_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        clone_group.add_argument('--name', '-n', help='Name of the Group')
        clone_group.add_argument('--secret', '-s', help='Name of the Secret')
        clone_group.add_argument('--newsecretname', '-nn', help='New name for the Secret')
        clone_group.add_argument('--content', '-c', help='Content of the Secret')
        clone_group.add_argument('--path', '-p', help='Path of the Secret')
        ## >>>>>>> Secrets Command >>>>>>> delete
        delete_secrets = secrets_args.add_parser('delete', help='Delete Secrets')
        delete_parser = delete_secrets.add_subparsers(dest='entity')
        delete_node = delete_parser.add_parser('node', help='Delete Node Secrets')
        delete_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        delete_node.add_argument('--name', '-n', help='Name of the Node')
        delete_node.add_argument('--secret', '-s', help='Name of the Secret')
        delete_group = delete_parser.add_parser('group', help='Delete Group Secrets')
        delete_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        delete_group.add_argument('--name', '-n', help='Name of the Group')
        delete_group.add_argument('--secret', '-s', help='Name of the Secret')
        return parser


    def list_secrets(self):
        """
        Method to list Secrets all or only node or
        only group depending on the arguments.
        """
        uri = self.route
        if 'name' in self.args:
            uri = f'{uri}/{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                uri = f'{uri}/{self.args["secret"]}'
        response = False
        get_list = Helper().get_list(uri)
        if get_list:
            data = get_list['config']['secrets']
            if self.args['raw']:
                response = Presenter().show_json(data)
            else:
                if 'group' in data:
                    table = f'group{self.route}'
                    fields, rows  =  Helper().get_secrets(table, data['group'])
                    response = Presenter().show_table(fields, rows)
                if 'node' in data:
                    table = f'node{self.route}'
                    fields, rows  =  Helper().get_secrets(table, data['node'])
                    response = Presenter().show_table(fields, rows)
        else:
            response = Helper().show_error(f'{self.route} is not found.')
        return response


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
            get_list = Helper().get_list(uri)
            if get_list:
                data = get_list['config']['secrets']
                if self.args['raw']:
                    response = Presenter().show_json(data)
                else:
                    if 'group' in data:
                        table = f'group{self.route}'
                        fields, rows  = Helper().filter_secret_col(table, data['group'])
                        group_name = list(data["group"].keys())[0]
                        title = f'Group {group_name} Secrets'
                        response = Presenter().show_table_col(title, fields, rows)
                    if 'node' in data:
                        table = f'node{self.route}'
                        fields, rows  = Helper().filter_secret_col(table, data['node'])
                        title = f'Node {self.args["name"]} Secrets'
                        response = Presenter().show_table_col(title, fields, rows)
        else:
            response = Helper().show_error('Either select node or group')
        return response


    def update_secrets(self):
        """
        Method to update Secrets for node or group
        depending on the arguments.
        """
        response = False
        if self.args['entity'] is not None:
            uri = f'{self.args["entity"]}/{self.args["name"]}'
            if self.args['secret'] is not None:
                if len(self.args["secret"]) == 1:
                    uri = f'{uri}/{self.args["secret"][0]}'
            payload = {}
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            del self.args['name']
            if self.args['init']:
                get_list = Helper().get_list(entity)
                if get_list:
                    names = list(get_list['config'][entity].keys())
                    entity_name = Inquiry().ask_select(f'Select {entity}', names)
                    def secrets(secret):
                        if len(secret):
                            confirm_text = "Add one more Secret?"
                        else:
                            confirm_text = "Add Secret?"
                        ifc = Inquiry().ask_confirm(confirm_text)
                        if ifc:
                            secret_name = Inquiry().ask_text("Write Secret Name")
                            content = Inquiry().ask_text("Write Secret Content")
                            path = Inquiry().ask_text("Write Secret Path")
                            if secret_name and content and path:
                                secret.append({
                                    'name': secret_name,
                                    'content': content,
                                    'path': path
                                })
                            return secrets(secret)
                        else:
                            return secret
                    secret = []
                    payload[entity_name] = secrets(secret)
                    table = f'{entity}{self.route}'
                    fields, rows  =  Helper().get_secrets(table, payload)
                    Presenter().show_table(fields, rows)
                    confirm = Inquiry().ask_confirm(f'Update {entity} => {entity_name.capitalize()} Secrets?')
                    if not confirm:
                        Helper().show_error(f'Update {entity} => {entity_name.capitalize()} Secrets Aborted')
            else:
                del self.args['debug']
                del self.args['command']
                del self.args['action']
                del self.args['init']
                if len(self.args['secret']) == len(self.args['content']) == len(self.args['path']):
                    self.args[entity_name] = []
                    temp_dict = {}
                    for secret, content, path in zip(self.args['secret'], self.args['content'], self.args['path']):
                        temp_dict['name'] = secret
                        temp_dict['content'] = content
                        temp_dict['path'] = path
                        self.args[entity_name].append(temp_dict)
                        temp_dict = {}
                    del self.args['secret']
                    del self.args['content']
                    del self.args['path']
                else:
                    response = Helper().show_error('Each Secret should have Secret Name, Content and Path')
                payload = self.args
            if payload:
                request_data = {}
                request_data['config'] = {}
                request_data['config'][self.route] = {}
                request_data['config'][self.route][entity] = {}
                request_data['config'][self.route][entity]= payload
                response = Rest().post_data(self.route, uri, request_data)
                if response == 201:
                    Helper().show_success(f'Secret for {entity} is created.')
                elif response == 204:
                    Helper().show_success(f'Secret for {entity} is update.')
                else:
                    Helper().show_error(f'HTTP ERROR: {response}.')
        else:
            response = Helper().show_error('Either select node or group')
        return response


    def clone_secrets(self):
        """
        Method to Clone Secrets for node or group
        depending on the arguments.
        """
        response = False
        secrets = []
        secret = {}
        old_secret_content, old_secret_path = '', ''
        if self.args['entity'] is not None:
            uri = f'{self.args["entity"]}/{self.args["name"]}/{self.args["secret"]}'
            payload = {}
            entity = self.args['entity']
            del self.args['entity']
            entity_name = self.args['name']
            del self.args['name']
            if self.args['init']:
                get_list = Helper().get_list(entity)
                if get_list:
                    names = list(get_list['config'][entity].keys())
                    entity_name = Inquiry().ask_select(f'Select {entity}', names)
                    get_list = Helper().get_list(self.route+'/'+entity+'/'+entity_name)
                    for sec in get_list['config'][self.route][entity][entity_name]:
                        secrets.append(sec['name'])
                        old_secret_content = sec['content']
                        old_secret_path = sec['path']
                    secret['name'] = Inquiry().ask_select('Select Secret to Clone', secrets)
                    secret['newsecretname'] = Inquiry().ask_text("Write a New Secret Name to Clone")
                    content = Inquiry().ask_text("Write Secret Content", True)
                    if content:
                        secret['content'] = content
                    else:
                        secret['content'] = old_secret_content
                    path = Inquiry().ask_text("Write Secret Content", True)
                    if path:
                        secret['path'] = path
                    else:
                        secret['path'] = old_secret_path
                    payload[entity_name] = [secret]
                    table = f'{entity}{self.route}'
                    print(table)
                    print(payload)
                    fields, rows  =  Helper().get_secrets(table, payload)
                    Presenter().show_table(fields, rows)
                    confirm = Inquiry().ask_confirm(f'Update {entity} => {entity_name.capitalize()} Secrets?')
                    if not confirm:
                        Helper().show_error(f'Update {entity} => {entity_name.capitalize()} Secrets Aborted')
            else:
                del self.args['debug']
                del self.args['command']
                del self.args['action']
                del self.args['init']
                get_list = Helper().get_list(self.route+'/'+entity+'/'+entity_name)
                for sec in get_list['config'][self.route][entity][entity_name]:
                    old_secret_content = sec['content']
                    old_secret_path = sec['path']
                secret = {}
                secret['name'] = self.args['secret']
                secret['newsecretname'] = self.args['newsecretname']
                if self.args['content']:
                    secret['content'] = self.args['content']
                else:
                    secret['content'] = old_secret_content
                if self.args['path']:
                    secret['path'] = self.args['path']
                else:
                    secret['path'] = old_secret_path
                payload[entity_name] = [secret]
            if payload:
                request_data = {}
                request_data['config'] = {}
                request_data['config'][self.route] = {}
                request_data['config'][self.route][entity] = {}
                request_data['config'][self.route][entity]= payload
                response = Rest().post_clone(self.route, uri, request_data)
                if response == 204:
                    Helper().show_success(f'Secret is Cloned.')
                else:
                    Helper().show_error(f'HTTP ERROR: {response}.')
        else:
            response = Helper().show_error('Either select node or group')
        return response


    def delete_secrets(self, args=None):
        """
        Method to update cluster in Luna Configuration.
        """
        return True
