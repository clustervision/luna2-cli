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
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

INI_FILE = '/trinity/local/luna/config/luna.ini'
LOG_FOLDER = '/var/log/luna'
PRE = "{Personal-Access-Token-Name}:{Personal-Access-Token}"

try: # for pip >= 10
    from pip._internal.req import parse_requirements
    install_requirements = list(parse_requirements('requirements.txt', session='hack'))
    requirements = [str(ir.requirement) for ir in install_requirements]
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    install_requirements = parse_requirements('requirements.txt', session='hack')
    requirements = [str(ir.req) for ir in install_requirements]


def new_version():
    """This Method will create a New version and update the Version file."""
    version = "0.0.0"
    with open('VERSION.txt', 'r', encoding='utf-8') as ver:
        version = ver.read()
    shutil.copy2('VERSION.txt', 'luna/VERSION.txt')
    return version


def create_dir(path=None):
    """This method will create required directories"""
    if os.path.exists(path) is False:
        try:
            os.makedirs(path, mode=0o777, exist_ok=False)
            sys.stdout.write(f'PASS :: {path} is created.\n')
        except PermissionError:
            sys.stderr.write('ERROR :: Install this tool as a super user.\n')
            sys.exit(1)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        create_dir(path="/trinity/local/luna/config")
        create_dir(path=LOG_FOLDER)
        if os.path.isfile(INI_FILE) is False:
            shutil.copy2('luna/luna.ini', INI_FILE)
        install.run(self)


setup(
	name = "luna",
	version = new_version(),
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
    cmdclass={'install': PostInstallCommand},
	install_requires = requirements,
	dependency_links = [],
	package_data = {"luna": ["*.txt", "*.ini"]},
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
