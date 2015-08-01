===============================
Skyscanner Python SDK
===============================

.. image:: https://api.travis-ci.org/Skyscanner/skyscanner-python-sdk.svg
    :target: https://travis-ci.org/Skyscanner/skyscanner-python-sdk

.. image:: https://img.shields.io/pypi/v/skyscanner.svg
    :target: https://pypi.python.org/pypi/skyscanner

Skyscanner Python SDK for Skyscanner's API

* Free software: BSD license
* SDK Documentation: https://skyscanner.readthedocs.org.
* API Documentation: http://business.skyscanner.net/portal/en-GB/Documentation/ApiOverview


Features
--------

* Tested on Python 2.6, 2.7, 3.3, 3.4
* Supports Flights, Hotels, and Carhire


Installation
------------

At the command line::

    $ easy_install skyscanner

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv skyscanner
    $ pip install skyscanner


Usage
-----

https://skyscanner.readthedocs.org/en/latest/usage.html  

Known Issues
------------

* Tests might appear to be broken sometimes, this is due to the throttling in the API. In such cases, you will see the following error in the build log:

        requests.exceptions.HTTPError: 429 Client Error: Too many requests in the last minute.
    
