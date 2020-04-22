========
Usage
========

To use Skyscanner Python SDK in a project, you will need to request an API key. Please use the following form: https://partners.skyscanner.net/contact/

Once you have an API key you can set it as follows:

        from skyscanner.skyscanner import Flights

        flights_service = Flights('<Your API Key>')


Flights: Live Pricing
~~~~~~~~~~~~~~~~~~~~~

https://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList

Get live prices::

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

Flights: Browse Cache
~~~~~~~~~~~~~~~~~~~~~

https://business.skyscanner.net/portal/en-GB/Documentation/FlightsBrowseCacheOverview

Cheapest quotes::

        from skyscanner.skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_quotes(
            market='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate='2017-05',
            inbounddate='2017-06').parsed

Cheapest price by route::

        from skyscanner.skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_price_by_route(
            market='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate='2017-05',
            inbounddate='2017-06').parsed

Cheapest price by date::

        from skyscanner.skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_price_by_date(
            market='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate='2017-05',
            inbounddate='2017-06').parsed

Grid of prices by date::

        from skyscanner.skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_grid_prices_by_date(
            market='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate='2017-05',
            inbounddate='2017-06').parsed

Car Hire
~~~~~~~~

https://business.skyscanner.net/portal/en-GB/Documentation/CarHireLivePricing

Get live prices::

        from skyscanner.skyscanner import CarHire

        carhire_service = CarHire('<Your API Key>')
        result = carhire_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            pickupplace='LHR-sky',
            dropoffplace='LHR-sky',
            pickupdatetime='2017-05-29T12:00',
            dropoffdatetime='2017-05-29T18:00',
            driverage='30',
            userip='175.156.244.174').parsed

Car hire autosuggest::

        from skyscanner.skyscanner import CarHire

        carhire_service = CarHire('<Your API Key>')
        result = carhire_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala').parsed

Hotels
~~~~~~

https://business.skyscanner.net/portal/en-GB/Documentation/HotelsOverview

Hotels autosuggest::

        from skyscanner.skyscanner import Hotels

        hotels_service = Hotels('<Your API Key>')
        result = hotels_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala').parsed

Hotels prices and details::

        from skyscanner.skyscanner import Hotels

        hotels_service = Hotels(self.api_key)
        result = hotels_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            entityid=27543923,
            checkindate='2017-05-26',
            checkoutdate='2017-05-30',
            guests=1,
            rooms=1).parsed
