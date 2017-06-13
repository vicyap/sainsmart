#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests==2.17.3'
]

setup_requirements = []

test_requirements = [
    'httmock==1.2.6',
    'requests==2.17.3'
]

setup(
    name='sainsmart',
    version='0.1.0',
    description="sainsmart contains code for working with sainsmart products.",
    long_description=readme + '\n\n' + history,
    author="Victor Yap",
    author_email='victor@vicyap.com',
    url='https://github.com/vicyap/sainsmart',
    packages=find_packages(include=['sainsmart']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='sainsmart',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
