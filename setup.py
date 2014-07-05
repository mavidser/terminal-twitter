#!/usr/bin/env python

from setuptools import setup

setup(
  name='Terminal Twitter',
  version='1.0',
  description='A Twitter CLI',
  author='Sid Verma',
  author_email='sid@sidverma.net',
  url='http://github.com/mavidser/tt',
  scripts=['app.py','keys.py'],
  install_requires=[
    'click==2.4',
    'tweepy==2.3.0'
  ],
  entry_points='''
    [console_scripts]
    tt=app:main
  ''',
)
