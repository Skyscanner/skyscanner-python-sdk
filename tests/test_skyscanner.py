# @Author: ardydedase <ardy.dedase@skyscanner.net>
# @Date:   2016-03-12 19:47:15
# @Last Modified by:   ardydedase
# @Last Modified time: 2016-04-25 11:15:49
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__credits__ = ["Ardy Dedase", "Denis Dudnik"]
__copyright__ = "Copyright (C) 2016 Skyscanner Ltd"
__license__ = """
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

"""
test_skyscanner
----------------------------------

Tests for `skyscanner` module.
"""

import unittest
import json
import pprint
from datetime import datetime, timedelta
from requests import HTTPError

from skyscanner.skyscanner import (Flights, Transport, FlightsCache,
                                   CarHire, Hotels,
                                   EmptyResponse, MissingParameter,
                                   STRICT, GRACEFUL, IGNORE)

# TODO: Mock responses


class SkyScannerTestCase(unittest.TestCase):

    """Generic TestCase class to support default failure messages."""

    def setUp(self):
        # This API Key is meant for tests only
        self.api_key = 'py495888586774232134437415165965'

        self.result = None

    def tearDown(self):
        self.result = None

    def assertTrue(self, expr, msg=None):
        super(SkyScannerTestCase, self).assertTrue(
            expr, msg=msg or self._default_message())

    def _default_message(self):
        return ('API Response: %s...' % (str(self.result)[:100])) if self.result is not None else None


class FakeResponse(object):

    def __init__(self, status_code=200, content=None):
        self.content = content or ''
        self.status_code = status_code

    def json(self):
        return json.loads(self.content)


class TestTransport(SkyScannerTestCase):

    def test_get_markets_json(self):
        transport = Transport(self.api_key, response_format='json')
        self.result = transport.get_markets('en-GB').parsed

        self.assertTrue('Countries' in self.result)
        self.assertTrue(len(self.result['Countries']) > 0)

    def test_get_markets_xml(self):
        transport = Transport(self.api_key, response_format='xml')
        self.result = transport.get_markets('de-DE').parsed

        self.assertTrue(None != self.result.find('./Countries'))
        self.assertTrue(len(self.result.findall('./Countries/CountryDto')) > 0)

    def test_location_autosuggest_json(self):
        transport = Transport(self.api_key, response_format='json')
        self.result = transport.location_autosuggest(query='KUL',
                                                     market='UK',
                                                     currency='GBP',
                                                     locale='en-GB').parsed

        self.assertTrue('Places' in self.result)
        self.assertTrue(len(self.result['Places']) > 0)

    def test_location_autosuggest_xml(self):
        transport = Transport(self.api_key, response_format='xml')
        self.result = transport.location_autosuggest(query='BER',
                                                     market='DE',
                                                     currency='EUR',
                                                     locale='de-DE').parsed

        self.assertTrue(None != self.result.find('./Places'))
        self.assertTrue(len(self.result.findall('./Places/PlaceDto')) > 0)

    def test_create_session(self):
        self.assertRaises(NotImplementedError,
                          Transport(self.api_key).create_session)

    def test_with_error_handling_strict(self):
        for format in ['json', 'xml']:
            try:
                self.assertRaises(RuntimeError,
                                  Transport._with_error_handling, FakeResponse(), RuntimeError, STRICT, format)

                self.assertRaises(HTTPError,
                                  Transport._with_error_handling, FakeResponse(status_code=404), HTTPError(), STRICT, format)

                self.assertRaises(HTTPError,
                                  Transport._with_error_handling, FakeResponse(status_code=429), HTTPError('429: '), STRICT, format)
                try:
                    Transport._with_error_handling(
                        FakeResponse(status_code=429), HTTPError('429: '), STRICT, format)
                except HTTPError as e:
                    self.assertEqual(
                        e.message, '429: Too many requests in the last minute.')

                self.assertRaises(HTTPError,
                                  Transport._with_error_handling, FakeResponse(status_code=400), HTTPError('400'), STRICT, format)
                try:
                    Transport._with_error_handling(
                        FakeResponse(status_code=400), HTTPError('400'), STRICT, format)
                except HTTPError as e:
                    self.assertEqual(e.message, '400')
            except Exception as e:
                # Exception for Python 2.6
                print(e)

        self.assertRaises(HTTPError,
                          Transport._with_error_handling, FakeResponse(status_code=400,
                                                                       content='{"ValidationErrors": '
                                                                       '[{"Message": "1"}, {"Message": "2"}]}'),
                          HTTPError('400'), STRICT, 'json')
        try:
            Transport._with_error_handling(FakeResponse(status_code=400,
                                                        content='{"ValidationErrors": '
                                                                '[{"Message": "1"}, {"Message": "2"}]}'),
                                           HTTPError('400'), STRICT, 'json')
        except HTTPError as e:
            try:
                self.assertEqual(
                    e.message, ('400: %s' % '\n\t'.join(['1', '2'])))
            except AttributeError as e:
                # Exception for Python 3
                print(e)

        try:
            self.assertRaises(HTTPError,
                              Transport._with_error_handling, FakeResponse(status_code=400,
                                                                           content='<Root><ValidationErrors>'
                                                                           '<ValidationErrorDto>'
                                                                           '<Message>1</Message'
                                                                           '</ValidationErrorDto>'
                                                                           '<ValidationErrorDto>'
                                                                           '<Message>2</Message'
                                                                           '</ValidationErrorDto>'
                                                                           '</ValidationErrors></Root>'),
                              HTTPError('400'), STRICT, 'xml')
        except Exception as e:
            # Exception for Python 2.6
            print(e)

        try:
            try:
                Transport._with_error_handling(FakeResponse(status_code=400,
                                                            content='<Root><ValidationErrors>'
                                                                    '<ValidationErrorDto>'
                                                                    '<Message>1</Message'
                                                                    '</ValidationErrorDto>'
                                                                    '<ValidationErrorDto>'
                                                                    '<Message>2</Message'
                                                                    '</ValidationErrorDto>'
                                                                    '</ValidationErrors></Root>'),
                                               HTTPError('400'), STRICT, 'xml')
            except Exception as e:
                # Exception for Python 2.6
                print(e)
        except HTTPError as e:
            try:
                self.assertEqual(e.message, '400')
            except AttributeError as e:
                # Exception for Python 3
                print(e)

    def test_with_error_handling_graceful(self):
        result = Transport._with_error_handling(
            FakeResponse(), EmptyResponse(), GRACEFUL, 'json')
        self.assertTrue(None != result)
        self.assertEqual(None, result.parsed)
        result = Transport._with_error_handling(
            FakeResponse(), EmptyResponse(), GRACEFUL, 'xml')
        self.assertTrue(None != result)
        self.assertEqual(None, result.parsed)

        result = Transport._with_error_handling(FakeResponse(content='{"valid": 1}', status_code=429),
                                                HTTPError(), GRACEFUL, 'json').parsed
        self.assertTrue(None != result)
        self.assertTrue('valid' in result)
        self.assertEqual(result['valid'], 1)
        result = Transport._with_error_handling(FakeResponse(content='<valid>1</valid>', status_code=429),
                                                HTTPError(), GRACEFUL, 'xml').parsed
        self.assertTrue(None != result)
        self.assertEqual(result.tag, 'valid')
        self.assertEqual(result.text, '1')

        result = Transport._with_error_handling(FakeResponse(content='invalid', status_code=429),
                                                HTTPError(), GRACEFUL, 'json').parsed
        self.assertEqual(None, result)

        try:
            result = Transport._with_error_handling(FakeResponse(content='invalid', status_code=429),
                                                    HTTPError(), GRACEFUL, 'xml').parsed
        except Exception as e:
            print(e)

        self.assertEqual(None, result)

        for format in ['json', 'xml']:
            self.assertRaises(HTTPError,
                              Transport._with_error_handling,
                              FakeResponse(), HTTPError(), GRACEFUL, format)
            self.assertRaises(RuntimeError,
                              Transport._with_error_handling,
                              FakeResponse(), RuntimeError(), GRACEFUL, format)

    def test_with_error_handling_ignore(self):
        result = Transport._with_error_handling(
            FakeResponse(), EmptyResponse(), IGNORE, 'json').parsed
        self.assertEqual(None, result)
        result = Transport._with_error_handling(
            FakeResponse(), RuntimeError(), IGNORE, 'json').parsed
        self.assertEqual(None, result)
        result = Transport._with_error_handling(
            FakeResponse(), HTTPError(), IGNORE, 'json').parsed
        self.assertEqual(None, result)

        try:
            result = Transport._with_error_handling(
                FakeResponse(), EmptyResponse(), IGNORE, 'xml').parsed
            self.assertEqual(None, result)
            result = Transport._with_error_handling(
                FakeResponse(), RuntimeError(), IGNORE, 'xml').parsed
            self.assertEqual(None, result)
            result = Transport._with_error_handling(
                FakeResponse(), HTTPError(), IGNORE, 'xml').parsed
            self.assertEqual(None, result)
        except Exception as e:
            # Exception for Python 2.6
            print(e)

        result = Transport._with_error_handling(
            FakeResponse(content='{"valid": 1}'), HTTPError(), IGNORE, 'json').parsed
        self.assertTrue(None != result)
        self.assertTrue('valid' in result)
        self.assertEqual(result['valid'], 1)
        result = Transport._with_error_handling(
            FakeResponse(content='<valid>1</valid>'), HTTPError(), IGNORE, 'xml').parsed
        self.assertTrue(None != result)
        self.assertEqual(result.tag, 'valid')
        self.assertEqual(result.text, '1')

    def test_default_resp_callback_json(self):
        t = Transport(self.api_key, response_format='json')
        self.assertRaises(EmptyResponse,
                          t._default_resp_callback, None)
        self.assertRaises(EmptyResponse,
                          t._default_resp_callback, FakeResponse(content=''))

        self.assertRaises(ValueError,
                          t._default_resp_callback, FakeResponse(content='invalid json'))

        resp_json = t._default_resp_callback(
            FakeResponse(content='{"valid": 1}')).parsed
        self.assertTrue(None != resp_json)
        self.assertTrue('valid' in resp_json)
        self.assertEqual(resp_json['valid'], 1)

    def test_default_resp_callback_xml(self):
        t = Transport(self.api_key, response_format='xml')
        self.assertRaises(EmptyResponse,
                          t._default_resp_callback, None)
        self.assertRaises(EmptyResponse,
                          t._default_resp_callback, FakeResponse(content=''))

        try:
            self.assertRaises(ValueError,
                              t._default_resp_callback, FakeResponse(content='invalid XML'))
        except:
            self.assertRaises(Exception,
                              t._default_resp_callback, FakeResponse(content='invalid XML'))

        resp_xml = t._default_resp_callback(
            FakeResponse(content='<valid a="test">1</valid>')).parsed
        self.assertTrue(None != resp_xml)
        self.assertEqual(resp_xml.tag, 'valid')
        self.assertEqual(resp_xml.text, '1')
        self.assertEqual(resp_xml.get('a'), 'test')

    def test_construct_params(self):
        params = dict(a=1, b=2, c=3)
        self.assertEqual(
            '1/2/3', Transport._construct_params(params, ('a', 'b', 'c')))
        params = dict(a=1, b=2)
        self.assertEqual(
            '1/2', Transport._construct_params(params, ('a', 'b'), ('c',)))
        params = dict(a=1, b=2, c=3)
        self.assertEqual(
            '1/2/3', Transport._construct_params(params, ('a', 'b'), ('c',)))

        params = dict(a=1, c=3)
        self.assertRaises(MissingParameter,
                          Transport._construct_params, params, ('a', 'b'), ('c',))


class TestCarHire(SkyScannerTestCase):

    def setUp(self):
        super(TestCarHire, self).setUp()
        datetime_format = '%Y-%m-%dT%H:%S'
        pickup_datetime = datetime.now() + timedelta(days=10)
        dropoff_datetime = pickup_datetime + timedelta(days=3)
        self.pickup = pickup_datetime.strftime(datetime_format)
        self.dropoff = dropoff_datetime.strftime(datetime_format)

    def test_location_autosuggest_json(self):
        carhire_service = CarHire(self.api_key, response_format='json')

        self.result = carhire_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala').parsed

        self.assertTrue('results' in self.result)
        self.assertTrue(len(self.result['results']) > 0)

    def test_location_autosuggest_xml(self):
        carhire_service = CarHire(self.api_key, response_format='xml')

        self.result = carhire_service.location_autosuggest(
            market='DE',
            currency='EUR',
            locale='de-DE',
            query='Berlin').parsed

        self.assertTrue(None != self.result.find('./Results'))
        self.assertTrue(
            len(self.result.findall('./Results/HotelResultDto')) > 0)

    def test_get_result_json(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """
        carhire_service = CarHire(self.api_key, response_format='json')

        self.result = carhire_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            pickupplace='LHR-sky',
            dropoffplace='LHR-sky',
            pickupdatetime=self.pickup,
            dropoffdatetime=self.dropoff,
            driverage='30',
            userip='175.156.244.174').parsed

        self.assertTrue('cars' in self.result)
        self.assertTrue('websites' in self.result)

    # def test_get_result_xml(self):
    #     """
    #     http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
    #     YYYY-MM-DDThh:mm
    #     """
    #     carhire_service = CarHire(self.api_key, response_format='xml')

    #     self.result = carhire_service.get_result(
    #         market='UK',
    #         currency='GBP',
    #         locale='en-GB',
    #         pickupplace='LHR-sky',
    #         dropoffplace='LHR-sky',
    #         pickupdatetime=self.pickup,
    #         dropoffdatetime=self.dropoff,
    #         driverage='30',
    #         userip='175.156.244.174').parsed

    #     self.assertTrue(None != self.result.find('./Cars'))
    #     self.assertTrue(None != self.result.find('./Websites'))

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
            pickupdatetime=self.pickup,
            dropoffdatetime=self.dropoff,
            driverage='30',
            userip='175.156.244.174')

        self.assertTrue(poll_url)


class TestHotels(SkyScannerTestCase):

    def setUp(self):
        super(TestHotels, self).setUp()
        datetime_format = '%Y-%m-%d'
        checkin_datetime = datetime.now()
        checkout_datetime = checkin_datetime + timedelta(days=4)
        self.checkin = checkin_datetime.strftime(datetime_format)
        self.checkout = checkout_datetime.strftime(datetime_format)

    def test_location_autosuggest_json(self):
        hotels_service = Hotels(self.api_key, response_format='json')

        self.result = hotels_service.location_autosuggest(
            market='UK',
            currency='GBP',
            locale='en-GB',
            query='Kuala').parsed

        self.assertTrue('results' in self.result)
        self.assertTrue(len(self.result['results']) > 0)

    def test_location_autosuggest_xml(self):
        hotels_service = Hotels(self.api_key, response_format='xml')

        self.result = hotels_service.location_autosuggest(
            market='DE',
            currency='EUR',
            locale='de-DE',
            query='Berlin').parsed

        self.assertTrue(None != self.result.find('./Results'))
        self.assertTrue(
            len(self.result.findall('./Results/HotelResultDto')) > 0)

    def test_get_result_json(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """

        hotels_service = Hotels(self.api_key, response_format='json')
        self.result = hotels_service.get_result(
            market='UK',
            currency='GBP',
            locale='en-GB',
            entityid=27543923,
            checkindate=self.checkin,
            checkoutdate=self.checkout,
            guests=1,
            rooms=1).parsed

        self.assertTrue('hotels' in self.result)
        self.assertTrue(len(self.result['hotels']) > 0)

    def test_get_result_xml(self):
        """
        http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
        YYYY-MM-DDThh:mm
        """

        hotels_service = Hotels(self.api_key, response_format='xml')
        self.result = hotels_service.get_result(
            market='DE',
            currency='EUR',
            locale='de-DE',
            entityid=27543923,
            checkindate=self.checkin,
            checkoutdate=self.checkout,
            guests=1,
            rooms=1).parsed

        self.assertTrue(None != self.result.find('./Hotels'))
        self.assertTrue(len(self.result.findall('./Hotels/HotelDto')) > 0)

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
            checkindate=self.checkin,
            checkoutdate=self.checkout,
            guests=1,
            rooms=1)

        self.assertTrue(poll_url)


class TestFlights(SkyScannerTestCase):

    def setUp(self):
        super(TestFlights, self).setUp()
        datetime_format = '%Y-%m'
        outbound_datetime = datetime.now() + timedelta(days=7)
        inbound_datetime = outbound_datetime + timedelta(days=31)
        self.outbound = outbound_datetime.strftime(datetime_format)
        self.inbound = inbound_datetime.strftime(datetime_format)

        datetime_format = '%Y-%m-%d'
        inbound_datetime = outbound_datetime + timedelta(days=3)
        self.outbound_days = outbound_datetime.strftime(datetime_format)
        self.inbound_days = inbound_datetime.strftime(datetime_format)

    def test_get_cheapest_quotes_json(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='json')
        self.result = flights_cache_service.get_cheapest_quotes(
            market='GB',
            currency='GBP',
            locale='en-GB',
            originplace='SIN',
            destinationplace='KUL',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue('Quotes' in self.result)
        self.assertTrue(len(self.result['Quotes']) > 0)

    def test_get_cheapest_quotes_xml(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='xml')
        self.result = flights_cache_service.get_cheapest_quotes(
            market='DE',
            currency='EUR',
            locale='de-DE',
            originplace='TXL',
            destinationplace='LHR',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue(None != self.result.find('./Quotes'))
        self.assertTrue(len(self.result.findall('./Quotes/QuoteDto')) > 0)

    def test_get_cheapest_price_by_route_json(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='json')
        self.result = flights_cache_service.get_cheapest_price_by_route(
            market='GB',
            currency='GBP',
            locale='en-GB',
            originplace='GB',
            destinationplace='DE',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue('Routes' in self.result)
        self.assertTrue(len(self.result['Routes']) > 0)

    def test_get_cheapest_price_by_route_xml(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='xml')
        self.result = flights_cache_service.get_cheapest_price_by_route(
            market='DE',
            currency='EUR',
            locale='de-DE',
            originplace='DE',
            destinationplace='GB',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue(None != self.result.find('./Routes'))
        self.assertTrue(len(self.result.findall('./Routes/RouteDto')) > 0)

    def test_get_cheapest_price_by_date_json(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='json')
        self.result = flights_cache_service.get_cheapest_price_by_date(
            market='GB',
            currency='GBP',
            locale='en-GB',
            originplace='SIN',
            destinationplace='KUL',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue('Quotes' in self.result)
        self.assertTrue(len(self.result['Quotes']) > 0)

    def test_get_cheapest_price_by_date_xml(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='xml')
        self.result = flights_cache_service.get_cheapest_price_by_date(
            market='DE',
            currency='EUR',
            locale='de-DE',
            originplace='TXL',
            destinationplace='LHR',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue(None != self.result.find('./Quotes'))
        self.assertTrue(len(self.result.findall('./Quotes/QuoteDto')) > 0)

    def test_get_grid_prices_by_date_json(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='json')
        self.result = flights_cache_service.get_grid_prices_by_date(
            market='GB',
            currency='GBP',
            locale='en-GB',
            originplace='SIN',
            destinationplace='KUL',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue('Dates' in self.result)
        self.assertTrue(len(self.result['Dates']) > 0)

    def test_get_grid_prices_by_date_xml(self):
        flights_cache_service = FlightsCache(
            self.api_key, response_format='xml')
        self.result = flights_cache_service.get_grid_prices_by_date(
            market='DE',
            currency='EUR',
            locale='de-DE',
            originplace='TXL',
            destinationplace='LHR',
            outbounddate=self.outbound,
            inbounddate=self.inbound).parsed

        self.assertTrue(None != self.result.find('./Dates'))
        self.assertTrue(len(self.result.findall('./Dates/ArrayOfCellDto')) > 0)

    def test_create_session(self):
        flights_service = Flights(self.api_key)
        poll_url = flights_service.create_session(
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound_days,
            inbounddate=self.inbound_days,
            adults=1)

        self.assertTrue(poll_url)

    def test_get_additional_params(self):
        flights_service = Flights(self.api_key)

        additional_params = flights_service.get_additional_params(
            stops=0,
            country='US',
            currency='USD',
            locale='en-US',
            originplace='DTW-sky',
            destinationplace='PEK-sky',
            outbounddate=self.outbound,
            inbounddate=self.inbound)
        self.assertEqual(additional_params, {'stops': 0})
    
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

    #     result = flights_service.request_booking_details(poll_url, outboundlegid=itinerary['OutboundLegId'],
    #                                                      inboundlegid=itinerary['InboundLegId'])

    #     print(result)

    #     pass

    def test_get_result_json(self):
        flights_service = Flights(self.api_key, response_format='json')
        self.result = flights_service.get_result(
            errors=GRACEFUL,
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            stops=1,
            outbounddate=self.outbound_days,
            inbounddate=self.inbound_days,
            adults=1).parsed

        self.assertTrue(None != self.result)
        self.assertTrue('Itineraries' in self.result)
        self.assertTrue(len(self.result['Itineraries']) > 0)

    def test_get_result_xml(self):
        flights_service = Flights(self.api_key, response_format='xml')
        self.result = flights_service.get_result(
            errors=GRACEFUL,
            country='UK',
            currency='GBP',
            locale='en-GB',
            originplace='SIN-sky',
            destinationplace='KUL-sky',
            outbounddate=self.outbound_days,
            inbounddate=self.inbound_days,
            adults=1).parsed

        self.assertTrue(None != self.result)
        self.assertTrue(None != self.result.find('./Itineraries'))
        self.assertTrue(
            len(self.result.findall('./Itineraries/ItineraryApiDto')) > 0)

if __name__ == '__main__':
    unittest.main()
