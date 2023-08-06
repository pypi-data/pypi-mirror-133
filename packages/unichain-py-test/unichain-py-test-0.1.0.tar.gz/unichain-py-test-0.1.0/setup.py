# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='unichain-py-test',
    version='0.1.0',
    description='Sample unichain-py-test by Python',
    long_description=readme,
    author='Real Elon Musk',
    author_email='realelonmusk102@gmail.com',
    url='https://github.com/kennethreitz/unichainpy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

