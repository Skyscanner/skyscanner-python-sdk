#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'requests'
]

test_requirements = [
    # TODO: put package test requirements here
    'requests'
]

setup(
    name='skyscanner',
    version='0.1.0',
    description="Skyscanner Python SDK",
    long_description=readme + '\n\n' + history,
    author="Ardy Dedase",
    author_email='ardy.dedase@gmail.com',
    url='https://github.com/ardydedase/skyscanner-python-sdk',
    packages=[
        'skyscanner',
    ],
    package_dir={'skyscanner':
                 'skyscanner'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='skyscanner',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
