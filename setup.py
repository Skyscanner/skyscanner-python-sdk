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
extras_requirements = {
    'Faster XML processing':  ["lxml"]
}
test_requirements = [
    # TODO: put package test requirements here
    'requests'
]

setup(
    name='skyscanner',
    version='1.1.2',
    description="Skyscanner Python SDK",
    long_description=readme + '\n\n' + history,
    author="Ardy Dedase",
    author_email='ardy.dedase@skyscanner.net',
    url='https://github.com/Skyscanner/skyscanner-python-sdk',
    packages=[
        'skyscanner',
    ],
    package_dir={'skyscanner':
                 'skyscanner'},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_requirements,
    license="Apache",
    zip_safe=False,
    keywords='skyscanner travel api business sdk flights hotels',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
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
