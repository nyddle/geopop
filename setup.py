#!/usr/bin/env python

from setuptools import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='geopop',
    version=version,
    description='Spatial population queries.',
    long_description=readme,
    author='Alexander Davydov',
    author_email='nyddle@gmail.com',
    packages=['geopop'],
    package_dir={'geopop': 'geopop'},
)

