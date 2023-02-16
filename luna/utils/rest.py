#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Microservice Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from configparser import RawConfigParser
import json
import os
import requests

class Rest(object):
    """
    All kind of REST Call methods.
    """

    def __init__(self):
        """
        Constructor - Before calling any REST API
        it will fetch the credentials and endpoint url
        from luna.ini from Luna 2 Daemon.
        """
        self.username, self.password, self.daemon = '', '', ''
        ini_file = '/trinity/local/luna/config/luna.ini'
        file_check = os.path.isfile(ini_file)
        read_check = os.access(ini_file, os.R_OK)
        if file_check and read_check:
            configparser = RawConfigParser()
            configparser.read(ini_file)
            if configparser.has_option('API', 'USERNAME'):
                self.username = configparser.get('API', 'USERNAME')
            if configparser.has_option('API', 'PASSWORD'):
                self.password = configparser.get('API', 'PASSWORD')
            if configparser.has_option('API', 'ENDPOINT'):
                self.daemon = configparser.get('API', 'ENDPOINT')
                # self.daemon = '127.0.0.1:7050'


    def get_token(self):
        """
        This method will fetch a valid token
        for further use.
        """
        data = {}
        response = False
        data['username'] = self.username
        data['password'] = self.password
        daemon_url = f'http://{self.daemon}/token'
        call = requests.post(url = daemon_url, json=data, timeout=5)
        data = call.json()
        if 'token' in data:
            response = data['token']
        return response

    def get_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        print(daemon_url)
        call = requests.get(url=daemon_url, params=data, timeout=5)
        print(call.content)
        print(call.status_code)
        if call:
            response = call.json()
        return response


    def post_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemonvia REST API's.
        And use for creating and updating records.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        call = requests.post(url=daemon_url, data=json.dumps(data), headers=headers, timeout=5)
        response = call.status_code
        return response


    def get_delete(self, table=None, name=None):
        """
        This method is based on REST API's GET method.
        It will delete the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        daemon_url = f'http://{self.daemon}/config/{table}/{name}/_delete'
        call = requests.get(url=daemon_url, timeout=5)
        response = call.status_code
        return response


    def post_clone(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemonvia REST API's.
        And use for cloning the records.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}/{name}/_clone'
        call = requests.post(url=daemon_url, data=json.dumps(data), headers=headers, timeout=5)
        response = call.status_code
        return response


    def get_status(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        call = requests.get(url=daemon_url, params=data, timeout=5)
        response = call.status_code
        return response


    def get_raw(self, route=None, uri=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        daemon_url = f'http://{self.daemon}/{route}'
        if uri:
            daemon_url = f'{daemon_url}/{uri}'
        response = requests.get(url=daemon_url, timeout=5)
        return response
