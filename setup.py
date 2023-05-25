#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup file, will build the pip package for the project.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "MIT"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"


import os
import sys
from setuptools import setup, find_packages

LOG_FOLDER = '/var/log/luna'
PRE = "{Personal-Access-Token-Name}:{Personal-Access-Token}"

if os.path.exists(LOG_FOLDER) is False:
    try:
        os.makedirs(LOG_FOLDER)
        sys.stdout.write(f'PASS :: {LOG_FOLDER} is created.\n')
    except PermissionError:
        sys.stderr.write('ERROR :: Install this tool as a super user.\n')
        sys.exit(1)


setup(
	name = "luna",
	version = __version__,
	description = "Luna CLI tool to manage Luna Daemon",
	long_description = "Luna CLI is a tool to manage Luna Daemon. It's a part of Trinity project.",
	author = "Sumit Sharma",
	author_email = "sumit.sharma@clustervision.com",
	maintainer = "Sumit Sharma",
	maintainer_email = "sumit.sharma@clustervision.com",
	url = "https://gitlab.taurusgroup.one/clustervision/luna2-cli.git",
	download_url = f"https://{PRE}@gitlab.taurusgroup.one/api/v4/projects/20/packages/pypi/simple",
	packages = find_packages(),
	license = "MIT",
	keywords = ["luna", "cli", "Trinity", "ClusterVision", "Sumit", "Sumit Sharma"],
	entry_points = {
		'console_scripts': [
			'luna = luna.cli:run_tool'
		]
	},
	dependency_links = [],
	package_data = {"luna": ["*.txt"]},
	data_files = [],
	zip_safe = False,
	include_package_data = True,
	classifiers = [
		'Development Status :: Beta',
		'Environment :: Console',
		'Intended Audience :: System Administrators',
		'License :: MIT',
		'Operating System :: RockyLinux :: CentOS :: RedHat',
		'Programming Language :: Python',
		'Topic :: Trinity :: Luna'
	],
	platforms = [
		'RockyLinux',
		'CentOS',
		'RedHat'
	]
)
# python setup.py sdist bdist_wheel
# python setup.py sdist bdist_rpm
