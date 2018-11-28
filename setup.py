#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
	name='pybpod-gui-plugin-soundcard',
	version="0.1",
	description="""PyBpod Sound card module controller""",
	author=['Luís Teixeira'],
	author_email='micboucinha@gmail.com',
	license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
	url='https://bitbucket.org/fchampalimaud/pybpod-soundcard-module',

	include_package_data=True,
	packages=find_packages(),

	package_data={'pybpod_soundcard_module': ['resources/*.*',]}
)