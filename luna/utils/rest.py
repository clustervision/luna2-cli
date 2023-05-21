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

import types
import base64
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from socket import timeout
import json
import binascii
import time
import os
import sys
from luna.utils.log import Log
from luna.utils.constant import INI_FILE, TOKEN_FILE
from luna.utils.message import Message
from luna.utils.configreader import ConfigReader

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
        self.username, self.password, self.daemon = self.get_ini_info()


    def get_data(self, table=None, name=None, data=None, raw_url=None):
        """
        This method will fetch the data from a URL.
        """
        response = types.SimpleNamespace()
        if raw_url:
            daemon_url = raw_url
        else:
            daemon_url = f'{self.daemon}/config/{table}'
            if name:
                daemon_url = f'{daemon_url}/{name}'
        try:
            request = Request(daemon_url)
            request.add_header('Content-Type', 'application/json; charset=utf-8')
            request.add_header('x-access-tokens', self.get_token())
            with urlopen(request, timeout=5) as result:
                read_response = result.read().decode('utf-8')
                if read_response:
                    read_response = json.loads(read_response)
                matches = ["delete", "/control/", "/_pack", "config/status/"]
                if any([x in daemon_url for x in matches]):
                    response.status = result.status
                    response.content = read_response
                else:
                    response = read_response
        except HTTPError as http_error:
            if '/control/' in daemon_url or '/_pack' in daemon_url or 'config/status/' in daemon_url and http_error.status == 404:
                response.status = 404
                response.content = ""
            else:
                reason = http_error.read().decode('utf-8')
                if reason:
                    reason = json.loads(reason)
                    if 'message' in reason:
                        reason = reason['message']
                else:
                    reason = http_error.reason
                Message().error_exit(f'ERROR :: {reason}', http_error.status)
        except URLError as url_error:
            if isinstance(url_error.reason, timeout):
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
            elif 'unknown url type' in url_error.reason:
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
            else:
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
        return response



    def post_url_data(self, table=None, name=None, data=None, raw_url=None):
        """
        This method will fetch the data from a URL.
        """
        response = types.SimpleNamespace()
        if raw_url:
            daemon_url = raw_url
        else:
            daemon_url = f'{self.daemon}/config/{table}'
            if name:
                daemon_url = f'{daemon_url}/{name}'
        try:
            request = Request(daemon_url)
            request.add_header('Content-Type', 'application/json; charset=utf-8')
            request.add_header('x-access-tokens', self.get_token())
            json_data = json.dumps(data)
            json_data_bytes = json_data.encode('utf-8')
            request.add_header('Content-Length', len(json_data_bytes))
            with urlopen(request, json_data_bytes, timeout=5) as result:
                read_response = result.read().decode('utf-8')
                if read_response:
                    read_response = json.loads(read_response)
                response.status = result.status
                response.content = read_response
        except HTTPError as http_error:
            reason = http_error.read().decode('utf-8')
            if reason and 'Internal Server Error' not in reason:
                reason = json.loads(reason)
                if 'message' in reason:
                    reason = reason['message']
            else:
                reason = http_error.reason
            Message().error_exit(f'ERROR :: {reason}', http_error.status)
        except URLError as url_error:
            if isinstance(url_error.reason, timeout):
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
            elif 'unknown url type' in url_error.reason:
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
            else:
                Message().error_exit(f'ERROR :: {daemon_url} {url_error.reason}')
        return response


    def decode_token(self, token=None):
        """
        This method decode the JWT token and validate it
        """
        valid = False
        api_expiry = 0
        current_time = int(time.time())
        try:
            token_meta = token.split(".")[0]
            token_meta_decoded = str(base64.b64decode(token_meta + "=="), "utf-8")
            json.loads(token_meta_decoded)
            token_payload = token.split(".")[1]
            token_payload_decoded = str(base64.b64decode(token_payload + "=="), "utf-8")
            payload = json.loads(token_payload_decoded)
            if 'exp' in payload:
                api_expiry = int(payload['exp'])
        except binascii.Error as decode_error:
            self.logger.debug(f'Token Decode Error :: {decode_error}')
        except UnicodeDecodeError as decode_error:
            self.logger.debug(f'Token Decode Error :: {decode_error}')
        except json.decoder.JSONDecodeError as decode_error:
            self.logger.debug(f'Token Decode Error :: {decode_error}')
        if current_time < api_expiry:
            valid = True
            self.logger.debug("TOKEN is Valid.")
        else:
            self.logger.debug("TOKEN is Expired")
        return valid


    def get_token(self):
        """
        This method will fetch a valid token for further use.
        """
        token_data = ""
        response = False
        if os.path.isfile(TOKEN_FILE):
            with open(TOKEN_FILE, 'r', encoding='utf-8') as token:
                token_data = token.read()
            check_token = self.decode_token(token_data)
            if check_token is True:
                response = token_data
            elif check_token is False:
                response = self.token()
        if response is False:
            response = self.token()
        return response


    def get_ini_info(self):
        """
        This method will get the information from the INI File.
        """
        errors = []
        file_check = os.path.isfile(INI_FILE)
        read_check = os.access(INI_FILE, os.R_OK)
        self.logger.debug(f'INI File => {INI_FILE} READ Check is {read_check}')
        if file_check and read_check:
            parser = ConfigReader()
            parser.read_file(INI_FILE)
            if parser.has_section('API'):
                self.username, errors = self.get_option(parser, errors, 'API', 'USERNAME')
                self.password, errors = self.get_option(parser, errors, 'API', 'PASSWORD')
                daemon, errors = self.get_option(parser, errors, 'API', 'ENDPOINT')
                protocol, errors = self.get_option(parser, errors, 'API', 'PROTOCOL')
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
        return self.username, self.password, self.daemon


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


    def token(self):
        """
        This method will fetch a valid token for further use.
        """
        data = {'username': self.username, 'password': self.password}
        token_url = f'{self.daemon}/token'
        try:
            request = Request(token_url)
            request.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(data)
            json_data_bytes = json_data.encode('utf-8')
            request.add_header('Content-Length', len(json_data_bytes))
            with  urlopen(request, json_data_bytes, timeout=5) as result:
                response = result.read().decode('utf-8')
                response = json.loads(response)
            if 'token' in response:
                response = response['token']
                with open(TOKEN_FILE, 'w', encoding='utf-8') as file_data:
                    file_data.write(response)
        except HTTPError as http_error:
            reason = http_error.read().decode('utf-8')
            if reason:
                reason = json.loads(reason)
                if 'message' in reason:
                    reason = reason['message']
            else:
                reason = http_error.reason
            Message().error_exit(f'ERROR :: {reason}', http_error.status)
        except URLError as url_error:
            if isinstance(url_error.reason, timeout):
                Message().error_exit(f'ERROR :: {token_url} {url_error.reason}')
            elif 'unknown url type' in url_error.reason:
                Message().error_exit(f'ERROR :: {token_url} {url_error.reason}')
            else:
                Message().error_exit(f'ERROR :: {token_url} {url_error.reason}')
        return response


    def get_delete(self, table=None, name=None):
        """
        This method is based on REST API's GET method.
        It will delete the records from Luna 2 Daemon via REST API's.
        """
        response = self.get_data(f'{table}/{name}/_delete')
        return response


    def post_clone(self, table=None, name=None, data=None):
        """
        This method is based on REST API's POST method.
        It will post data to Luna 2 Daemon via REST API's.
        And use for cloning the records.
        """
        response = self.post_url_data(f'{table}/{name}/_clone', None, data)
        return response


    def get_raw(self, route=None, uri=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon via REST API's.
        """
        daemon_url = f'{self.daemon}/{route}'
        if uri:
            daemon_url = f'{daemon_url}/{uri}'
        response = self.get_data(None, None, None, daemon_url)
        return response


    def post_raw(self, route=None, payload=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon via REST API's.
        """
        response = self.post_url_data(None, None, payload, f'{self.daemon}/{route}')
        return response
