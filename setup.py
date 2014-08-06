#!/usr/bin/env python

from setuptools import setup
from sys import platform as OPERATING_SYSTEM

if OPERATING_SYSTEM == "win32":
  packages = [
    'click==2.4',
    'tweepy==2.3.0',
    'colorama==0.3.1'
  ]
else:
  packages = [
    'click==2.4',
    'tweepy==2.3.0'
  ]

setup(
  name='Terminal Twitter',
  version='1.0',
  description='A Twitter CLI',
  author='Sid Verma',
  author_email='sid@sidverma.net',
  url='http://github.com/mavidser/tt',
  scripts=['app.py','keys.py'],
  install_requires=packages,
  entry_points='''
    [console_scripts]
    tt=app:main
  ''',
)
