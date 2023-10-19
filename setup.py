#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2023  ClusterVision Solutions b.v.
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
Setup file, will build the pip package for the project.
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Development"

from time import time
from setuptools import setup, find_packages

PRE = "{Personal-Access-Token-Name}:{Personal-Access-Token}"

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
    install_requirements = list(parse_requirements('requirements.txt', session='hack'))
    requirements = [str(ir.requirement) for ir in install_requirements]
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements
    install_requirements = parse_requirements('requirements.txt', session='hack')
    requirements = [str(ir.req) for ir in install_requirements]


def new_version():
    """
    This Method will create a New version and update the Version file.
    """
    time_now = int(time())
    version = f'2.0.{time_now}'
    with open('luna/VERSION.txt', 'w', encoding='utf-8') as ver:
        ver.write(version)
    return version


setup(
	name = "luna2-cli",
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
		'License :: GPL',
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
