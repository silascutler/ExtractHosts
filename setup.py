#!/usr/bin/env python3

from distutils.core import setup

setup(name='Extracthosts',
      version='2.0.0',
      description='Extracts IPs and domain names from files',
      author='Brian Wallace',
      author_email='bwall@ballastsecurity.net',
      url='https://github.com/bwall/ExtractHosts',
      packages=['ExtractHosts'],
      scripts=['eh'],
     )