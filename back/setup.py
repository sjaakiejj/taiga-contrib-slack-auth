#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-slack-auth',
    version = ":versiontools:taiga_contrib_slack_auth:",
    description = "The Taiga plugin for slack authentication",
    long_description = "",
    keywords = 'taiga, slack, auth, plugin',
    author = 'Jacobus Meulen',
    author_email = 'jacobus@openbusiness.com.sg',
    url = 'https://github.com/sjaakiejj/taiga-contrib-slack-auth',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
