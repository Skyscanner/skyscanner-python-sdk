===============================
Skyscanner Python SDK
===============================

.. image:: https://api.travis-ci.org/Skyscanner/skyscanner-python-sdk.svg
    :target: https://travis-ci.org/Skyscanner/skyscanner-python-sdk

.. image:: https://img.shields.io/pypi/v/skyscanner.svg
    :target: https://pypi.python.org/pypi/skyscanner

.. image:: https://readthedocs.org/projects/skyscanner/badge/?version=latest
        :target: https://readthedocs.org/projects/skyscanner/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/Skyscanner/skyscanner-python-sdk/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/Skyscanner/skyscanner-python-sdk?branch=master


Skyscanner Python SDK for Skyscanner's API

* Free software: Apache license
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


Quick start
-----------

1. Request for an API Key from `Skyscanner for Business Contact Page`_.
2. Set your API Key::

    from skyscanner import Flights
    flights_service = Flights('<Your API Key>')

3. Get the flights live pricing result by writing a few lines of code::

    from skyscanner import Flights

    flights_service = Flights('<Your API Key>')
    result = flights_service.get_result(
        country='UK',
        currency='GBP',
        locale='en-GB',
        originplace='SIN-sky',
        destinationplace='KUL-sky',
        outbounddate='2016-07-28',
        inbounddate='2016-07-31',
        adults=1).parsed

    print(result)

Note that both the ``inbounddate`` and ``outbounddate`` might need to be updated.

.. _Skyscanner for Business Contact Page: http://en.business.skyscanner.net/en-gb/contact/


More examples
-------------

For more example usage, `refer to our documentation`_.

.. _refer to our documentation: https://skyscanner.readthedocs.org/en/latest/usage.html
  

Known Issues
------------

* Tests might appear to be broken sometimes, this is due to the throttling in the API. In such cases, you will see the following error in the build log::

        requests.exceptions.HTTPError: 429 Client Error: Too many requests in the last minute.
    
