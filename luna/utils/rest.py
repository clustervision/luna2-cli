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

import requests
# from luna.utils.helper import Helper
import os
import json
from configparser import RawConfigParser

class Rest(object):
    """
    All kind of REST Call methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """
        # token = False
        self.username, self.password, self.daemon = '', '', ''
        ini_file = '/trinity/local/luna/config/luna.ini'
        file_check = os.path.isfile(ini_file)
        read_check = os.access(ini_file, os.R_OK)
        if file_check and read_check:
            configParser = RawConfigParser()
            configParser.read(ini_file)
            if configParser.has_option('API', 'USERNAME'):
                self.username = configParser.get('API', 'USERNAME')
            if configParser.has_option('API', 'PASSWORD'):
                self.password = configParser.get('API', 'PASSWORD')
            if configParser.has_option('API', 'ENDPOINT'):
                self.daemon = configParser.get('API', 'ENDPOINT')


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
        call = requests.post(url = daemon_url, json=data)
        data = call.json()
        if 'token' in data:
            response = data['token']
        return response

    def get_data(self, table=None, name=None, data=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        response = False
        daemonip, daemonport = '192.168.164.90', '7050'
        daemon_url = f'http://{daemonip}:{daemonport}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        call = requests.get(url=daemon_url, params=data)
        if call:
            response = call.json()
        return response


    def post_data(self, table=None, name=None, data=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        response = False
        headers = {'x-access-tokens': self.get_token()}
        daemon_url = f'http://{self.daemon}/config/{table}'
        if name:
            daemon_url = f'{daemon_url}/{name}'
        call = requests.post(url=daemon_url, data=json.dumps(data), headers=headers)
        response = call.status_code
        return response
