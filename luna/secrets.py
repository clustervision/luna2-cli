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

6. luna secrets show -R
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
        update_node.add_argument('name', help='Name of the Node')
        update_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        update_node.add_argument('--secret', '-s', help='Name of the Secret')
        update_node.add_argument('--content', '-c', help='Content of the Secret')
        update_node.add_argument('--path', '-p', help='Path of the Secret')
        update_group = update_parser.add_parser('group', help='Update Group Secrets')
        update_group.add_argument('name', help='Name of the Group')
        update_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        update_group.add_argument('--secret', '-s', help='Name of the Secret')
        update_group.add_argument('--content', '-c', help='Content of the Secret')
        update_group.add_argument('--path', '-p', help='Path of the Secret')
        ## >>>>>>> Secrets Command >>>>>>> clone
        clone_secrets = secrets_args.add_parser('clone', help='Clone Secrets')
        clone_parser = clone_secrets.add_subparsers(dest='entity')
        clone_node = clone_parser.add_parser('node', help='Clone Node Secrets')
        clone_node.add_argument('name', help='Name of the Node')
        clone_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        clone_node.add_argument('--secret', '-s', help='Name of the Secret')
        clone_node.add_argument('--newsecretname', '-n', help='New name for the Secret')
        clone_node.add_argument('--content', '-c', help='Content of the Secret')
        clone_node.add_argument('--path', '-p', help='Path of the Secret')
        clone_group = clone_parser.add_parser('group', help='Clone Group Secrets')
        clone_group.add_argument('name', help='Name of the Group')
        clone_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        clone_group.add_argument('--secret', '-s', help='Name of the Secret')
        clone_group.add_argument('--newsecretname', '-n', help='New name for the Secret')
        clone_group.add_argument('--content', '-c', help='Content of the Secret')
        clone_group.add_argument('--path', '-p', help='Path of the Secret')
        ## >>>>>>> Secrets Command >>>>>>> delete
        delete_secrets = secrets_args.add_parser('delete', help='Delete Secrets')
        delete_parser = delete_secrets.add_subparsers(dest='entity')
        delete_node = delete_parser.add_parser('node', help='Delete Node Secrets')
        delete_node.add_argument('name', help='Name of the Node')
        delete_node.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
        delete_node.add_argument('--secret', '-s', help='Name of the Secret')
        delete_group = delete_parser.add_parser('group', help='Delete Group Secrets')
        delete_group.add_argument('name', help='Name of the Group')
        delete_group.add_argument('--init', '-i', action='store_true', help='Secret values one-by-one')
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
        Method to show Secrets all or only node or
        only group depending on the arguments.
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


    def update_secrets(self, args=None):
        """
        Method to update cluster in Luna Configuration.
        """
        return True


    def clone_secrets(self, args=None):
        """
        Method to update cluster in Luna Configuration.
        """
        return True


    def delete_secrets(self, args=None):
        """
        Method to update cluster in Luna Configuration.
        """
        return True
