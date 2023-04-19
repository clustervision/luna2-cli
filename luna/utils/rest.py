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
__status__      = "Development"

from configparser import RawConfigParser
import os
import sys
import requests
from luna.utils.log import Log

class Rest():
    """
    All kind of REST Call methods.
    """

    def __init__(self):
        """
        Constructor - Before calling any REST API
        it will fetch the credentials and endpoint url
        from luna.ini from Luna 2 Daemon.
        """
        self.error_msg = []
        self.logger = Log.get_logger()
        self.username, self.password, self.daemon = None, None, None
        ini_file = '/trinity/local/luna/config/luna.ini'
        file_check = os.path.isfile(ini_file)
        read_check = os.access(ini_file, os.R_OK)
        self.logger.debug(f'INI File => {ini_file} READ Check is {read_check}')
        if file_check and read_check:
            configparser = RawConfigParser()
            configparser.read(ini_file)
            if configparser.has_section('API'):
                if configparser.has_option('API', 'USERNAME'):
                    self.username = configparser.get('API', 'USERNAME')
                else:
                    self.error_msg.append(f'USERNAME is not found in API section in {ini_file}.')
                if configparser.has_option('API', 'PASSWORD'):
                    self.password = configparser.get('API', 'PASSWORD')
                else:
                    self.error_msg.append(f'PASSWORD is not found in API section in {ini_file}.')
                if configparser.has_option('API', 'ENDPOINT'):
                    self.daemon = configparser.get('API', 'ENDPOINT')
                else:
                    self.error_msg.append(f'ENDPOINT is not found in API section in {ini_file}.')
            else:
                self.error_msg.append(f'API section is not found in {ini_file}.')
        else:
            self.error_msg.append(f'{ini_file} is not found on this machine.')
        if self.error_msg:
            print("You need to fix following errors...")
            num = 1
            for error in self.error_msg:
                print(f'{num}. {error}')
            sys.exit(1)


    def get_token(self):
        """
        This method will fetch a valid token
        for further use.
        """
        data = {}
        response = False
        if os.path.isfile('/tmp/token.txt'):
            with open('/tmp/token.txt', 'r', encoding='utf-8') as token:
                token_data = token.read()
                if len(token_data):
                    response = token_data
        else:
            data['username'] = self.username
            data['password'] = self.password
            daemon_url = f'http://{self.daemon}/token'
            self.logger.debug(f'Token URL => {daemon_url}')
            try:
                call = requests.post(url = daemon_url, json=data, timeout=5)
                self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
                data = call.json()
                if 'token' in data:
                    response = data['token']
                    with open('/tmp/token.txt', 'w', encoding='utf-8') as file_data:
                        file_data.write(response)
            except requests.exceptions.ConnectionError:
                sys.stderr.write(f'ERROR :: Unable to Coonect Luna Daemon => http://{self.daemon}.')
                self.logger.debug(f'ERROR :: Unable to connect Luna Daemon http://{self.daemon}.')
                sys.exit(1)
        return response


    def reset_token(self):
        """
        This method will update the token
        """
        data = {}
        response = False
        data['username'] = self.username
        data['password'] = self.password
        daemon_url = f'http://{self.daemon}/token'
        self.logger.debug(f'Token URL => {daemon_url}')
        try:
            call = requests.post(url = daemon_url, json=data, timeout=5)
            self.logger.debug(f'Response {call.content}& HTTP Code {call.status_code}')
            data = call.json()
            if 'token' in data:
                response = data['token']
                with open('/tmp/token.txt', 'w', encoding='utf-8') as file_data:
                    file_data.write(response)
            elif 'message' in data:
                sys.stderr.write(f'ERROR :: {data["message"]}.')
                self.logger.debug(f'ERROR :: {data["message"]}.')
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            sys.stderr.write(f'ERROR :: Unable to Coonect Luna Daemon => http://{self.daemon}.')
            self.logger.debug(f'ERROR :: Unable to connect Luna Daemon => http://{self.daemon}.')
            sys.exit(1)
        return response

    def get_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            call = requests.get(url=daemon_url, params=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
            response_json = call.json()
            if 'message' in response_json:
                sys.stderr.write(f'{response_json["message"]}.')
                sys.exit(1)
            else:
                response = response_json
        except requests.exceptions.JSONDecodeError:
            response = False
        except ValueError:
            self.reset_token()
            response = self.get_data(table, name, data)
        return response


    def post_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemonvia REST API's.
        And use for creating and updating records.
        """
        response = False
        headers = {'x-access-tokens': self.get_token(), 'Content-Type':'application/json'}
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'POST URL => {daemon_url}')
        self.logger.debug(f'POST DATA => {data}')
        try:
            response = requests.post(url=daemon_url, json=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except ValueError:
            self.reset_token()
            response = self.post_data(table, name, data)
        return response


    def get_delete(self, table=None, name=None):
        """
        This method is based on REST API's GET method.
        It will delete the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}/{name}/_delete'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            response = requests.get(url=daemon_url, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except ValueError:
            self.reset_token()
            response = self.get_delete(table, name)
        return response


    def post_clone(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemonvia REST API's.
        And use for cloning the records.
        """
        response = False
        headers = {'x-access-tokens': self.get_token(), 'Content-Type':'application/json'}
        daemon_url = f'http://{self.daemon}/config/{table}/{name}/_clone'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = requests.post(url=daemon_url, json=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except ValueError:
            self.reset_token()
            response = self.post_clone(table, name, data)
        return response


    def get_status(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'Status URL => {daemon_url}')
        try:
            call = requests.get(url=daemon_url, params=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
            response = call.status_code
        except ValueError:
            self.reset_token()
            response = self.get_status(table, name, data)
        return response


    def get_raw(self, route=None, uri=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/{route}'
        if uri:
            daemon_url = f'{daemon_url}/{uri}'
        self.logger.debug(f'RAW URL => {daemon_url}')
        try:
            response = requests.get(url=daemon_url, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except ValueError:
            self.reset_token()
            response = self.get_raw(route, uri)
        return response


    def post_raw(self, route=None, payload=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon
        via REST API's.
        """
        response = False
        headers = {'x-access-tokens': self.get_token(), 'Content-Type':'application/json'}
        daemon_url = f'http://{self.daemon}/{route}'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = requests.post(url=daemon_url, json=payload, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except ValueError:
            self.reset_token()
            response = self.post_raw(route, payload)
        return response
