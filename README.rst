===============================
Skyscanner Python SDK
===============================

You will need to contact us to request an API key to use our APIs via the following form: https://partners.skyscanner.net/contact. 

We receive a large number of requests and although we do our best to reply to all we cannot guarantee that your application will be successful. 

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
* API Documentation: https://business.skyscanner.net/portal/en-GB/Documentation/ApiOverview


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

1. Contact us to request an API key: https://partners.skyscanner.net/contact
2. If you don't already have one, create a `Skyscanner account`_.
3. Sign into your account and click 'Import Existing App' and use your API key to create an App
4. Set your API Key in your code::

    from skyscanner.skyscanner import Flights
    flights_service = Flights('<Your API Key>')

5. Get the flights live pricing result by writing a few lines of code::

    from skyscanner.skyscanner import Flights

    flights_service = Flights('<Your API Key>')
    result = flights_service.get_result(
        country='UK',
        currency='GBP',
        locale='en-GB',
        originplace='SIN-sky',
        destinationplace='KUL-sky',
        outbounddate='2017-05-28',
        inbounddate='2017-05-31',
        adults=1).parsed

    print(result)

Note that both the ``inbounddate`` and ``outbounddate`` might need to be updated.

.. _Skyscanner account: https://partners.skyscanner.net/log-in/


More examples
-------------

For more example usage, refer to the `SDK documentation`_ or the `API documentation`_.

.. _SDK documentation: https://skyscanner.readthedocs.org/en/latest/usage.html
.. _API documentation: https://skyscanner.github.io/slate/
  

Known Issues
------------

* Tests might appear to be broken sometimes, this is due to the throttling in the API. In such cases, you will see the following error in the build log::

        requests.exceptions.HTTPError: 429 Client Error: Too many requests in the last minute.

* Please allow up to 15 minutes for your API key to be activated. Until it is activated you will get a 403 exception::
        
        requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://partners.api.skyscanner.net/apiservices/pricing/v1.0?apiKey=<Your API key>

    
