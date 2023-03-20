#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup file, will build the pip package for the project.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

import os
import sys
LOG_FOLDER = '/var/log/luna'
from setuptools import setup, find_packages

try: # for pip >= 10
    from pip._internal.req import parse_requirements
    install_reqs = list(parse_requirements('requirements.txt', session='hack'))
    reqs = [str(ir.requirement) for ir in install_reqs]
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    install_reqs = parse_requirements('requirements.txt', session='hack')
    reqs = [str(ir.req) for ir in install_reqs]

if os.path.exists(LOG_FOLDER) is False:
    try:
        os.makedirs(LOG_FOLDER)
        print(f'ERROR :: {LOG_FOLDER} is created.')
    except PermissionError:
        print("ERROR :: Install this tool as a super user.")
        sys.exit(1)
else:
    print("NO-IMPACT :: Log Directory already present.")


setup(
    name="luna2-cli",
	version = "2.0",
	description = "Luna2 CLI is a command line utility",
	url = "https://gitlab.taurusgroup.one/clustervision/luna2-cli.git",
	author = "Sumit Sharma",
	author_email = "sumit.sharma@clustervision.com",
	license = "MIT",
	packages = find_packages(),
	install_requires = reqs,
	entry_points = {
    	'console_scripts': [
		'luna = luna.cli:run_tool'
		]
	},
	dependency_links = [],
	package_data = {},
	data_files = [],
	zip_safe = False,
	include_package_data = True
)
# python setup.py sdist bdist_wheel
