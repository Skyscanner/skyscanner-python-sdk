#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_skyscanner
----------------------------------

Tests for `skyscanner` module.
"""

import unittest

from skyscanner.skyscanner import Flights, Transport, FlightsCache, CarHire, Hotels

class TestCarHire(unittest.TestCase):
    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart
        self.api_key = 'prtl6749387986743898559646983194'
        pass

    def test_location_autosuggest(self):
        carhire_service = CarHire(self.api_key)

        result = carhire_service.location_autosuggest(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            query='Kuala')

        self.assertTrue(len(result['results']) > 0)

    def test_get_result(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip} 
        YYYY-MM-DDThh:mm
        """
        carhire_service = CarHire(self.api_key)

        result = carhire_service.get_result(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            pickupplace='LHR-sky', 
            dropoffplace='LHR-sky', 
            pickupdatetime='2015-05-25T12:00', 
            dropoffdatetime='2015-05-25T18:00', 
            driverage='30',
            userip='175.156.244.174')

        self.assertTrue(('cars' in result) and ('websites' in result))

    def test_create_session(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip} 
        YYYY-MM-DDThh:mm
        """
        carhire_service = CarHire(self.api_key)

        poll_url = carhire_service.create_session(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            pickupplace='LHR-sky', 
            dropoffplace='LHR-sky', 
            pickupdatetime='2015-05-28T12:00', 
            dropoffdatetime='2015-05-31T12:00', 
            driverage='30',
            userip='175.156.244.174')

        self.assertTrue(poll_url)

    def tearDown(self):
        pass        
        

class TestHotels(unittest.TestCase):
    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart

        self.api_key = 'prtl6749387986743898559646983194'
        pass

    def test_location_autosuggest(self):
        hotels_service = Hotels(self.api_key)

        result = hotels_service.location_autosuggest(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            query='Kuala')

        self.assertTrue(len(result['results']) > 0)

    def test_get_result(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip} 
        YYYY-MM-DDThh:mm
        """

        hotels_service = Hotels(self.api_key)
        result = hotels_service.get_result(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            entityid=27543923, 
            checkindate='2015-05-26', 
            checkoutdate='2015-05-30', 
            guests=1, 
            rooms=1)

        self.assertTrue(len(result['places']) > 0)

    def test_create_session(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip} 
        YYYY-MM-DDThh:mm
        """
        hotels_service = Hotels(self.api_key)

        poll_url = hotels_service.create_session(
            market='UK', 
            currency='GBP', 
            locale='en-GB', 
            entityid=27543923, 
            checkindate='2015-05-26', 
            checkoutdate='2015-05-30', 
            guests=1, 
            rooms=1)

        self.assertTrue(poll_url)

    def tearDown(self):
        pass        


class TestFlights(unittest.TestCase):

    def setUp(self):
        # API Key that's meant for testing only
        # Taken from: http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingQuickStart

        self.api_key = 'prtl6749387986743898559646983194'
        pass

    def test_get_cheapest_quotes(self):
        flights_cache_service = FlightsCache(self.api_key)
        result = flights_cache_service.get_cheapest_quotes(
            country='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06')

        self.assertTrue(len(result['Quotes']) > 0)        


    # I'm getting the following result:
    # {u'ValidationErrors': [{u'Message': u'For this query please use the following service [BrowseDates]'}]}        
    def test_get_cheapest_price_by_route(self):
        flights_cache_service = FlightsCache(self.api_key)
        result = flights_cache_service.get_cheapest_price_by_route(
            country='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06')

        print("result: %s" % result)


    def test_get_cheapest_price_by_date(self):
        flights_cache_service = FlightsCache(self.api_key)
        result = flights_cache_service.get_cheapest_price_by_date(
            country='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06')

        self.assertTrue(len(result['Quotes']) > 0)

    def test_get_grid_prices_by_date(self):
        flights_cache_service = FlightsCache(self.api_key)
        result = flights_cache_service.get_grid_prices_by_date(
            country='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05', 
            inbounddate='2015-06')

        self.assertTrue(len(result['Dates']) > 0)


    def test_create_session(self):
        flights_service = Flights(self.api_key)
        poll_url = flights_service.create_session(
            country='UK',
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05-28', 
            inbounddate='2015-05-31', 
            adults=1)

        self.assertTrue(poll_url)

    def test_get_markets(self):
        transport = Transport(self.api_key)
        result = transport.get_markets('en-GB')

        self.assertTrue(len(result['Countries']) > 0)

    def test_location_autosuggest(self):
        transport = Transport(self.api_key)
        result = transport.location_autosuggest('KUL', 'UK', 'GBP', 'en-GB')

        self.assertTrue(len(result['Places']) > 0)


    # def test_poll_session(self):
    #     flights_service = Flights(self.api_key)

    #     poll_url = flights_service.create_session(
    #         country='UK', 
    #         currency='GBP', 
    #         locale='en-GB', 
    #         originplace='SIN-sky', 
    #         destinationplace='KUL-sky', 
    #         outbounddate='2015-05-28', 
    #         inbounddate='2015-05-31', 
    #         adults=1)

    #     result = flights_service.poll_session(poll_url, sorttype='carrier')

    #     self.assertTrue(len(result['Itineraries']) > 0)

    #     pass

    # def test_request_booking_details(self):
    #     flights_service = Flights(self.api_key)

    #     poll_url = flights_service.create_session(
    #         country='UK', 
    #         currency='GBP', 
    #         locale='en-GB', 
    #         originplace='SIN-sky', 
    #         destinationplace='KUL-sky', 
    #         outbounddate='2015-05-28', 
    #         inbounddate='2015-05-31', 
    #         adults=1)

    #     flights_results = flights_service.poll_session(poll_url, sorttype='carrier')

    #     print(flights_results)

    #     itinerary = flights_results['Itineraries'][0]

    #     result = flights_service.request_booking_details(poll_url, outboundlegid=itinerary['OutboundLegId'], inboundlegid=itinerary['InboundLegId'])

    #     print(result)

    #     pass            

    def test_get_result(self):
        flights_service = Flights(self.api_key)
        result = flights_service.get_result(
            country='UK', 
            currency='GBP', 
            locale='en-GB', 
            originplace='SIN-sky', 
            destinationplace='KUL-sky', 
            outbounddate='2015-05-28', 
            inbounddate='2015-05-31', 
            adults=1)

        # print(result)
        print("status: %s" % result['Status'])
        # self.assertTrue(len(result['Flights']['Itineraries']) > 0)        


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()