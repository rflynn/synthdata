#!/usr/bin/env python3

from distutils.core import setup

setup(name='synthdata',
      version='0.0',
      description='Synthesize data sets from existing data sets',
      author='Ryan Flynn',
      author_email='parseerror+synthdata@gmail.com',
      url='',
      packages=['synthdata'],
      test_suite='nose.collector',
      tests_require=['nose'],
)
