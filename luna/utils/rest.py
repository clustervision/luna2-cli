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


import json
import types
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
        Constructor - Before calling any REST API it will fetch the credentials and endpoint url
        from luna.ini from Luna 2 Daemon.
        """
        self.logger = Log.get_logger()
        self.username, self.password, self.daemon, self.secret_key = self.get_ini_info()


    def get_ini_info(self):
        """
        This method will get the information from the INI File.
        """
        errors = []
        file_check = os.path.isfile(INI_FILE)
        read_check = os.access(INI_FILE, os.R_OK)
        self.logger.debug(f'INI File => {INI_FILE} READ Check is {read_check}')
        if file_check and read_check:
            parser = RawConfigParser()
            parser.read(INI_FILE)
            if parser.has_section('API'):
                self.username, errors = self.get_option(parser, errors, 'API', 'USERNAME')
                self.password, errors = self.get_option(parser, errors, 'API', 'PASSWORD')
                self.secret_key, errors = self.get_option(parser, errors, 'API', 'SECRET_KEY')
                protocol, errors = self.get_option(parser, errors, 'API', 'PROTOCOL')
                daemon, errors = self.get_option(parser, errors, 'API', 'ENDPOINT')
                self.daemon = f'{protocol}://{daemon}'
            else:
                errors.append(f'API section is not found in {INI_FILE}.')
        else:
            errors.append(f'{INI_FILE} is not found on this machine.')
        if errors:
            Message().show_error('You need to fix following errors...')
            num = 1
            for error in errors:
                Message().show_error(f'{num}. {error}')
                num = num + 1
            sys.exit(1)
        return self.username, self.password, self.daemon, self.secret_key


    def get_option(self, parser=None, error=None, section=None, option=None):
        """
        This method will retrieve the value from the INI
        """
        response = False
        if parser.has_option(section, option):
            response = parser.get(section, option)
        else:
            error.append(f'{option} is not found in {section} section in {INI_FILE}.')
        return response, error
    

    def get_response(self, data=None):
        """
        This method will return the response object.
        """
        if data.content:
            response = types.SimpleNamespace()
            response.status_code = data.status_code
            try:
                json_message = data.json()
                if 'message' in json_message:
                    response.content = json_message['message']
                elif 'token' in json_message:
                    response.content = json_message['token']
                else:
                    response.content = json_message
            except requests.exceptions.JSONDecodeError:
                response.content = data.content
        else:
            response = data
        return response


    def token(self):
        """
        This method will fetch a valid token for further use.
        """
        data = {'username': self.username, 'password': self.password}
        daemon_url = f'{self.daemon}/token'
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
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        daemon_url = f'{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            call = requests.get(url=daemon_url, params=data, headers=headers, timeout=5)
            self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
            response = self.get_response(call)
            # response_json = call.json()
            # if 'message' in response_json:
            #     Message().show_error(response_json["message"])
            # else:
            #     response = response_json
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
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
        daemon_url = f'{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'POST URL => {daemon_url}')
        self.logger.debug(f'POST DATA => {data}')
        try:
            response = requests.post(url=daemon_url, json=data, headers=headers, timeout=5)
            response = self.get_response(response)
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
        daemon_url = f'{self.daemon}/config/{table}/{name}/_delete'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            response = requests.get(url=daemon_url, headers=headers, timeout=5)
            response = self.get_response(response)
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
        daemon_url = f'{self.daemon}/config/{table}/{name}/_clone'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = requests.post(url=daemon_url, json=data, headers=headers, timeout=5)
            response = self.get_response(response)
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
        daemon_url = f'{self.daemon}/config/{table}'
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
        daemon_url = f'{self.daemon}/{route}'
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
        daemon_url = f'{self.daemon}/{route}'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = requests.post(url=daemon_url, json=payload, headers=headers, timeout=5)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response
