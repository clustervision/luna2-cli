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

class Rest(object):
    """
    All kind of REST Call methods.
    """

    def __init__(self):
        """
        Constructor - As of now, nothing have to initialize.
        """


    def get_data(self, table=None, data=None):
        """
        This method will fetch all records from
        the Luna 2 Daemon Database
        """
        daemonip, daemonport = '', ''
        daemon_url = f'http://{daemonip}:{daemonport}/config/{table}'
        call = requests.get(url=daemon_url, params=data)
        data = call.json()
        print(data)
        return True


    def post_data(self, table=None, data=None):
        """
        This method will fetch a records from
        the Luna 2 Daemon Database
        """
        daemonip, daemonport, token = '', '' , ''
        data['token'] = token
        daemon_url = f'http://{daemonip}:{daemonport}/config/{table}'
        call = requests.post(url = daemon_url, params=data)
        data = call.json()
        print(data)
        return True
