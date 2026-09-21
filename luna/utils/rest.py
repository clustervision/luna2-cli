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
Microservice Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2025, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.2"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"


import types
from configparser import RawConfigParser
import os
import sys
import requests
from requests import Session
from requests.adapters import HTTPAdapter
import jwt
import urllib3
from urllib3.util import Retry
from luna.utils.log import Log
from luna.utils.constant import INI_FILE, TOKEN_FILE, USER_INI_FILE, USER_TOKEN_FILE
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
        self.ini_file, self.token_file = self.credential_files()
        self.username,self.password,self.daemon,self.secret_key,self.security = self.get_ini_info()
        urllib3.disable_warnings()
        self.request_timeout = 20
        self.security = True if self.security.lower() in ['y', 'yes', 'true']  else False
        self.session = Session()
        # read=0 on purpose. A read timeout means the connection was made and the
        # daemon simply has not answered yet - the request landed, and a control
        # action is not idempotent, so repeating it can power-cycle a node twice.
        # It also arrives as extra load on a daemon that is by definition already
        # slow, which is the opposite of backing off. A failed *connection* is
        # different: nothing was delivered, so those are still worth retrying.
        self.retries = Retry(
            total=6,
            connect=6,
            read=0,
            status=6,
            backoff_factor=0.2,
            status_forcelist=[502, 503, 504],
            allowed_methods={'GET', 'POST'},
        )
        self.session.mount('https://', HTTPAdapter(max_retries=self.retries))


    def daemon_validation(self, parser=None):
        """
        This method will fetch a valid token for further use.
        """
        check = False
        exception = 'ERROR'
        daemon_url = f'{self.daemon}/version'
        self.logger.debug(f'URL {daemon_url}')
        try:
            response = requests.get(url=daemon_url, timeout=20, verify=False)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            check = True
            self.logger.debug(f'{exception} :: {ssl_loop_error}')
        except requests.exceptions.ConnectionError as conn_error:
            check = True
            self.logger.debug(f'{exception} :: {conn_error}')
        except requests.exceptions.ReadTimeout as time_error:
            check = True
            self.logger.debug(f'{exception} :: {time_error}')
        if check is True and parser is not True:
            exception = f'ERROR :: Unable to reach {daemon_url} Try again or check the config'
            Message().error_exit(exception)
        return check


    @staticmethod
    def credential_files():
        """
        The person's own login first, the controller's file second, and the token cache
        follows the file that was used: root on the controller keeps the shared token as
        today, a person who ran luna login holds their own.
        """
        user_ini = os.path.expanduser(USER_INI_FILE)
        if os.path.isfile(user_ini) and os.access(user_ini, os.R_OK):
            return user_ini, os.path.expanduser(USER_TOKEN_FILE)
        return INI_FILE, TOKEN_FILE

    def get_ini_info(self):
        """
        This method will get the information from the INI File.
        """
        errors = []
        ini_file = self.ini_file
        file_check = os.path.isfile(ini_file)
        read_check = os.access(ini_file, os.R_OK)
        self.logger.debug(f'INI File => {ini_file} READ Check is {read_check}')
        if file_check and read_check:
            parser = RawConfigParser()
            parser.read(ini_file)
            if parser.has_section('API'):
                self.username, errors = self.get_option(parser, errors, 'API', 'USERNAME')
                self.password, errors = self.get_option(parser, errors, 'API', 'PASSWORD')
                # the signing key stays on the daemon; a client reads expiry unverified
                self.secret_key = parser.get('API', 'SECRET_KEY', fallback=None)
                protocol, errors = self.get_option(parser, errors, 'API', 'PROTOCOL')
                daemon, errors = self.get_option(parser, errors, 'API', 'ENDPOINT')
                self.daemon = f'{protocol}://{daemon}'
                self.security, errors = self.get_option(parser, errors, 'API', 'VERIFY_CERTIFICATE')
            else:
                errors.append(f'API section is not found in {ini_file}.')
        else:
            errors.append(f'{ini_file} is not found on this machine, and no {USER_INI_FILE}: run luna login')
        if errors:
            Message().show_error('You need to fix following errors...')
            num = 1
            for error in errors:
                Message().show_error(f'{num}. {error}')
                num = num + 1
            sys.exit(1)
        return self.username, self.password, self.daemon, self.secret_key, self.security


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


    def send(self, method=None, url=None, **kwargs):
        """
        One request with the cached token. A 401 means the daemon no longer accepts the
        token (expired on its clock, user disabled, key rotated): log in once and resend.
        The token is never inspected here beyond its expiry; the daemon decides.
        """
        extra = {'Content-Type': 'application/json'} if 'json' in kwargs else {}
        kwargs['headers'] = {'x-access-tokens': self.get_token(), **extra}
        response = getattr(self.session, method)(url, **kwargs)
        if response.status_code == 401:
            self.logger.debug('Token refused by the daemon, logging in again once.')
            kwargs['headers'] = {'x-access-tokens': self.token(), **extra}
            response = getattr(self.session, method)(url, **kwargs)
        return response

    def get_response(self, data=None):
        """
        This method will return the response object.
        """
        if data.content:
            response = types.SimpleNamespace()
            response.status_code = data.status_code
            try:
                json_message = data.json()
                if 'request_id' in json_message:
                    response.content = json_message
                elif 'message' in json_message:
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
            call = self.session.post(
                daemon_url,
                json=data,
                stream=True,
                timeout=self.request_timeout,
                verify=self.security
            )
            self.logger.debug(f'Response {call.content} & HTTP Code {call.status_code}')
            if call.content:
                data = call.json()
                if 'token' in data:
                    response = data['token']
                    try:
                        self.store_token(response)
                    except PermissionError as exp:
                        Message().error_exit(str(exp))
                elif 'message' in data:
                    Message().error_exit(data["message"], call.status_code)
            else:
                Message().error_exit(call.content, call.status_code)
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        except requests.exceptions.JSONDecodeError:
            Message().error_exit(call.content, call.status_code)
        return response


    def store_token(self, token=None):
        """
        The token cache beside the credential file that was used, readable by its owner only.
        """
        directory = os.path.dirname(self.token_file)
        try:
            if directory and not os.path.isdir(directory):
                os.makedirs(directory, mode=0o700, exist_ok=True)
            with open(self.token_file, 'w', encoding='utf-8') as file_data:
                file_data.write(token)
            os.chmod(self.token_file, 0o600)
        except PermissionError as exp:
            # somebody else's cache, root's on a controller: say so where a person can act on it
            raise PermissionError(f'{self.token_file} is not yours to write: run luna login to work as yourself') from exp

    def get_token(self):
        """
        This method will fetch a valid token for further use. Expiry is read from the token
        without verifying the signature: the key stays on the daemon, which is the only place
        a token's validity is decided. A refused token is renewed by logging in again.
        """
        response = False
        if os.path.isfile(self.token_file):
            with open(self.token_file, 'r', encoding='utf-8') as token:
                token_data = token.read()
            try:
                jwt.decode(token_data, options={'verify_signature': False, 'verify_exp': True, 'require': ['exp']})
                response = token_data
            except jwt.exceptions.ExpiredSignatureError:
                self.logger.debug('Expired Signature Error, Getting New Token.')
                response = self.token()
            except jwt.exceptions.PyJWTError as exp:
                # unreadable, or without an expiry claim: not ours to keep
                self.logger.debug(f'Token unusable ({exp}), Getting New Token.')
                response = self.token()
        if response is False:
            response = self.token()
        return response


    def get_data(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon  via REST API's.
        """
        response = False
        daemon_url = f'{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{self.daemon}/config/{table}/{name}'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            response = self.send(
                'get', daemon_url,
                params=data,
                stream=True,
                timeout=self.request_timeout,
                verify=self.security
            )
            response = self.get_response(response)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
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
        daemon_url = f'{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'POST URL => {daemon_url}')
        self.logger.debug(f'POST DATA => {data}')
        try:
            response = self.send(
                'post', daemon_url,
                json=data,
                stream=True,                timeout=self.request_timeout,
                verify=self.security
            )
            response = self.get_response(response)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response


    def get_delete(self, table=None, name=None):
        """
        This method is based on REST API's GET method.
        It will delete the records from Luna 2 Daemon via REST API's.
        """
        response = False
        daemon_url = f'{self.daemon}/config/{table}/{name}/_delete'
        self.logger.debug(f'GET URL => {daemon_url}')
        try:
            response = self.send(
                'get', daemon_url,
                stream=True,
                timeout=self.request_timeout,
                verify=self.security
            )
            response = self.get_response(response)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
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
        daemon_url = f'{self.daemon}/config/{table}/{name}/_clone'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = self.send(
                'post', daemon_url,
                json=data,
                stream=True,                timeout=self.request_timeout,
                verify=self.security
            )
            response = self.get_response(response)
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response


    def get_status(self, table=None, name=None, data=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon via REST API's.
        """
        response = False
        daemon_url = f'{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        self.logger.debug(f'Status URL => {daemon_url}')
        try:
            response = self.send(
                'get', daemon_url,
                params=data,
                stream=True,
                timeout=self.request_timeout,
                verify=self.security
            )
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
            response = response.status_code
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response


    def get_raw(self, route=None, uri=None, noexit=False, timeout=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon via REST API's.
        A caller whose request is known to be slow to answer may pass its own
        timeout; the default is the one every other request uses.
        """
        response = False
        daemon_url = f'{self.daemon}/{route}'
        if uri:
            daemon_url = f'{daemon_url}/{uri}'
        self.logger.debug(f'RAW URL => {daemon_url}')
        try:
            response = self.send(
                'get', daemon_url,
                stream=True,
                timeout=timeout or self.request_timeout,
                verify=self.security
            )
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            if noexit:
                Message().show_error(f'Request Timeout while {daemon_url}')
            else:
                Message().error_exit(f'Request Timeout while {daemon_url}')
        return response


    def post_raw(self, route=None, payload=None):
        """
        This method is based on REST API's GET method.
        It will fetch the records from Luna 2 Daemon via REST API's.
        """
        response = False
        daemon_url = f'{self.daemon}/{route}'
        self.logger.debug(f'Clone URL => {daemon_url}')
        try:
            response = self.send(
                'post', daemon_url,
                json=payload,
                stream=True,                timeout=self.request_timeout,
                verify=self.security
            )
            self.logger.debug(f'Response {response.content} & HTTP Code {response.status_code}')
        except requests.exceptions.SSLError as ssl_loop_error:
            self.logger.debug(f'SSLError => {ssl_loop_error}')
        except requests.exceptions.ConnectionError:
            Message().error_exit(f'Request Timeout while {daemon_url}')
        return response
