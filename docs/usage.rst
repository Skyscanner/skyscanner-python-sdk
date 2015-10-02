========
Usage
========

To use Skyscanner Python SDK in a project, make sure that you set your API Key. For example::

        from skyscanner import Flights
        
        flights_service = Flights('<Your API Key>')        


Flights: Live Pricing
~~~~~~~~~~~~~~~~~~~~~

http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList

Get live prices::

        from skyscanner import Flights
        
        flights_service = Flights('<Your API Key>')
        result = flights_service.get_result(
            country='UK', 
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05-28', 
            inbounddate='2015-05-31', 
            adults=1).parsed

Flights: Browse Cache
~~~~~~~~~~~~~~~~~~~~~

http://business.skyscanner.net/portal/en-GB/Documentation/FlightsBrowseCacheOverview

Cheapest quotes::

        from skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_quotes(
            market='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06').parsed

Cheapest price by route::

        from skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_price_by_route(
            market='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06').parsed

Cheapest price by date::

        from skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_cheapest_price_by_date(
            market='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06').parsed

Grid of prices by date::

        from skyscanner import FlightsCache

        flights_cache_service = FlightsCache('<Your API Key>')
        result = flights_cache_service.get_grid_prices_by_date(
            market='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06').parsed

Car Hire
~~~~~~~~

http://business.skyscanner.net/portal/en-GB/Documentation/CarHireLivePricing

Get live prices::
    
        from skyscanner import CarHire

        carhire_service = CarHire('<Your API Key>')
        result = carhire_service.get_result(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            pickupplace='LHR-sky', 
            dropoffplace='LHR-sky', 
            pickupdatetime='2015-05-29T12:00', 
            dropoffdatetime='2015-05-29T18:00', 
            driverage='30',
            userip='175.156.244.174').parsed

Car hire autosuggest::

        from skyscanner import CarHire

        carhire_service = CarHire('<Your API Key>')
        result = carhire_service.location_autosuggest(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            query='Kuala').parsed

Hotels
~~~~~~

http://business.skyscanner.net/portal/en-GB/Documentation/HotelsOverview

Hotels autosuggest::
    
        from skyscanner import Hotels

        hotels_service = Hotels('<Your API Key>')
        result = hotels_service.location_autosuggest(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            query='Kuala').parsed

Hotels prices and details::

        from skyscanner import Hotels

        hotels_service = Hotels(self.api_key)
        result = hotels_service.get_result(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            entityid=27543923, 
            checkindate='2015-05-26', 
            checkoutdate='2015-05-30', 
            guests=1, 
            rooms=1).parsed