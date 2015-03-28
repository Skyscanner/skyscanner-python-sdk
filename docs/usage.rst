========
Usage
========

To use Skyscanner Python SDK in a project::

Flights: Live Pricing::

API Documentation: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList

Get live prices::

    from skyscanner.skyscanner import Flights    

    # Get Flights Live Pricing result
    flights_service = Flights('<Your API Key>')

    result = flights_service.get_result(
        country='UK', 
        currency='GBP', 
        locale='en-GB', 
        originplace='SIN-sky', 
        destinationplace='KUL-sky', 
        outbounddate='2015-05-28', 
        inbounddate='2015-05-31', 
        adults=1)

Browse Cache Overview::

    from skyscanner.skyscanner import FlightsCache

    flights_cache_service = FlightsCache('<Your API Key>')
    result = flights_cache_service.get_cheapest_quotes(
        country='UK',
        currency='GBP', 
        locale='en-GB', 
        originplace='SIN-sky', 
        destinationplace='KUL-sky', 
        outbounddate='2015-05', 
        inbounddate='2015-06')

Cheapest quotes::

    flights_cache_service = FlightsCache('<Your API Key>')
    result = flights_cache_service.get_cheapest_price_by_route(
        country='UK',
        currency='GBP', 
        locale='en-GB', 
        originplace='SIN-sky', 
        destinationplace='KUL-sky', 
        outbounddate='2015-05', 
        inbounddate='2015-06')
