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
import jwt
from luna.utils.log import Log
from luna.utils.constant import INI_FILE, TOKEN_FILE
from luna.utils.message import Message

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
        self.username, self.password, self.daemon, self.secret_key = None, None, None, None
        file_check = os.path.isfile(INI_FILE)
        read_check = os.access(INI_FILE, os.R_OK)
        self.logger.debug(f'INI File => {INI_FILE} READ Check is {read_check}')
        if file_check and read_check:
            configparser = RawConfigParser()
            configparser.read(INI_FILE)
            if configparser.has_section('API'):
                if configparser.has_option('API', 'USERNAME'):
                    self.username = configparser.get('API', 'USERNAME')
                else:
                    self.error_msg.append(f'USERNAME is not found in API section in {INI_FILE}.')
                if configparser.has_option('API', 'PASSWORD'):
                    self.password = configparser.get('API', 'PASSWORD')
                else:
                    self.error_msg.append(f'PASSWORD is not found in API section in {INI_FILE}.')
                if configparser.has_option('API', 'ENDPOINT'):
                    self.daemon = configparser.get('API', 'ENDPOINT')
                else:
                    self.error_msg.append(f'ENDPOINT is not found in API section in {INI_FILE}.')
                if configparser.has_option('API', 'SECRET_KEY'):
                    self.secret_key = configparser.get('API', 'SECRET_KEY')
                else:
                    self.error_msg.append(f'SECRET_KEY is not found in API section in {INI_FILE}.')
            else:
                self.error_msg.append(f'API section is not found in {INI_FILE}.')
        else:
            self.error_msg.append(f'{INI_FILE} is not found on this machine.')
        if self.error_msg:
            Message().show_error('You need to fix following errors...')
            num = 1
            for error in self.error_msg:
                Message().show_error(f'{num}. {error}')
            sys.exit(1)


    def token(self):
        """
        This method will fetch a valid token for further use.
        """
        data = {'username': self.username, 'password': self.password}
        daemon_url = f'http://{self.daemon}/token'
        self.logger.debug(f'Token URL => {daemon_url}')
        try:
            call = requests.post(url=daemon_url, json=data, timeout=5)
            self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
            if call.content:
                data = call.json()
                if 'token' in data:
                    response = data['token']
                    with open(TOKEN_FILE, 'w', encoding='utf-8') as file_data:
                        file_data.write(response)
                elif 'message' in data:
                    Message().error_exit(data["message"], call.status_code)
            else:
                Message().error_exit(call.content, call.status_code)
        except requests.exceptions.ConnectionError:
            Message().error_exit(call.content, call.status_code)
        except requests.exceptions.JSONDecodeError:
            Message().error_exit(call.content, call.status_code)
        return response


    def get_token(self):
        """
        This method will fetch a valid token
        for further use.
        """
        response = False
        if os.path.isfile(TOKEN_FILE):
            with open(TOKEN_FILE, 'r', encoding='utf-8') as token:
                token_data = token.read()
            try:
                jwt.decode(token_data, self.secret_key, algorithms=['HS256'])
                response = token_data
            except jwt.exceptions.DecodeError:
                self.logger.debug('Token Decode Error, Getting New Token.')
                response = self.token()
            except jwt.exceptions.ExpiredSignatureError:
                self.logger.debug('Expired Signature Error, Getting New Token.')
                response = self.token()
        if response is False:
            response = self.token()
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
                Message().show_error(response_json["message"])
            else:
                response = response_json
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}', call.status_code)
        except requests.exceptions.JSONDecodeError:
            response = False
        return response


    def post_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemon via REST API's.
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
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response


    def post_clone(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemon via REST API's.
        And use for cloning the records.
        """
        response = False
        headers = {'x-access-tokens': self.get_token(), 'Content-Type':'application/json'}
        daemon_url = f'http://{self.daemon}/config/{table}/{name}/_clone'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = requests.post(url=daemon_url, json=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response
