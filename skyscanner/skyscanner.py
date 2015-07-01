# -*- coding: utf-8 -*-
import requests
import time
import socket


class ExceededRetries(Exception):
    pass


class ResponseException(Exception):
    pass


class Transport(object):

    """
    Parent class for initialization
    """
    API_HOST = 'http://partners.api.skyscanner.net'
    MARKET_SERVICE_URL = '{api_host}/apiservices/reference/v1.0/countries'.format(api_host=API_HOST)
    LOCATION_AUTOSUGGEST_SERVICE_URL = '{api_host}/apiservices/autosuggest/v1.0'.format(api_host=API_HOST)

    def __init__(self, api_key):
        if not api_key:
            raise ValueError('API key must be specified.')
        self.api_key = api_key

    def get_result(self, **params):
        """
        Get all results, no filtering, etc. by creating and polling the session.
        """
        return self.poll_session(self.create_session(**params))

    def make_request(self, service_url, method='get', headers=None, data=None, callback=None, **params):
        """
        Reusable method for simple GET requests
        """
        if callback is None:
            callback = self._default_resp_callback

        if 'apikey' not in service_url.lower():
            params.update({
                'apiKey': self.api_key
            })

        request = getattr(requests, method.lower())
        r = request(service_url, headers=headers, data=data, params=params)

        return callback(r)

    def get_markets(self, market):
        """
        Get the list of markets
        http://business.skyscanner.net/portal/en-GB/Documentation/Markets
        """
        url = "{url}/{market}".format(url=self.MARKET_SERVICE_URL,
                                      market=market)

        return self.make_request(url)

    def location_autosuggest(self, query, market, currency, locale):
        """
        Location Autosuggest Service
        Doc URL: http://business.skyscanner.net/portal/en-GB/Documentation/Autosuggest
        Format: {API_HOST}/apiservices/autosuggest/v1.0/{market}/{currency}/{locale}/?query={query}&apiKey={apiKey}
        """

        url = "{url}/{market}/{currency}/{locale}/".format(url=self.LOCATION_AUTOSUGGEST_SERVICE_URL,
                                                           market=market, currency=currency, locale=locale)

        return self.make_request(url, query=query)

    def get_poll_response(self, poll_url, **params):
        return self.make_request(poll_url, **params)

    def create_session(self, **params):
        """Creates a session for polling. Should be implemented by sub-classes"""
        raise NotImplementedError('Should be implemented by a sub-class.')

    def poll_session(self, poll_url, initial_delay=2, delay=1, tries=10, **params):
        """
        Poll the URL
        :param poll_url - URL to poll, should be returned by 'create_session' call
        :param initial_delay - specifies how many seconds to wait before the first poll
        :param delay - specifies how many seconds to wait between the polls
        :param tries - number of polls to perform
        :param params - additional query params for each poll request
        """
        time.sleep(initial_delay)
        for n in range(tries):
            try:
                poll_response = self.get_poll_response(poll_url, **params)

                if self.is_poll_complete(poll_response):
                    return poll_response
                else:
                    time.sleep(delay)

            except socket.error as e:
                raise RuntimeError("Connection dropped with error code {0}".format(e.errno))
        raise ExceededRetries("Failed to poll within {0} tries.".format(tries))

    def is_poll_complete(self, poll_resp):
        """
        Checks the condition in poll response to determine if it is complete
        and no subsequent poll requests should be done.
        """
        success_list = ['UpdatesComplete', True, 'COMPLETE']
        status = poll_resp.get('Status', poll_resp.get('status'))
        if not status:
            raise RuntimeError('Unable to get poll response status.')
        return status in success_list

    @staticmethod
    def _default_session_headers():
        return {'content-type': 'application/x-www-form-urlencoded',
                'accept': 'application/json'}

    @staticmethod
    def _default_resp_callback(resp):
        try:
            resp_json = resp.json()
        except ValueError:
            raise ValueError('Invalid JSON in response: %s' % resp.content)

        if 'errors' in resp_json:
            errors = resp_json['errors']
            msg = '\n\t%s' % '\n\t'.join(errors) if len(errors) > 1 else errors[0]
            raise ResponseException(msg)

        return resp_json


class Flights(Transport):

    """
    Flights Live Pricing
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/pricing/v1.0'.format(api_host=Transport.API_HOST)

    def __init__(self, api_key):
        Transport.__init__(self, api_key)

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-mm-dd
        location: ISO code
        """
        return self.make_request(self.PRICING_SESSION_URL,
                                 method='post',
                                 headers=self._default_session_headers(),
                                 callback=lambda resp: resp.headers['location'],
                                 data=params)

    def request_booking_details(self, poll_url, **params):
        """
        Request for booking details
        URL Format: {API_HOST}/apiservices/pricing/v1.0/{session key}/booking?apiKey={apiKey}
        """
        return self.make_request("%s/booking" % poll_url,
                                 method='put',
                                 callback=lambda resp: resp.headers['location'],
                                 **params)


class FlightsCache(Flights):

    """
    Flights Browse Cache
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsBrowseCacheOverview
    """

    BROWSE_QUOTES_SERVICE_URL = '{api_host}/apiservices/browsequotes/v1.0'.format(api_host=Transport.API_HOST)
    BROWSE_ROUTES_SERVICE_URL = '{api_host}/apiservices/browseroutes/v1.0'.format(api_host=Transport.API_HOST)
    BROWSE_DATES_SERVICE_URL = '{api_host}/apiservices/browsedates/v1.0'.format(api_host=Transport.API_HOST)
    BROWSE_GRID_SERVICE_URL = '{api_host}/apiservices/browsegrid/v1.0'.format(api_host=Transport.API_HOST)

    def construct_params(self, params):
        """
        Construct params list in order
        """
        params_list = [params['country'], params['currency'], params['locale'], params[
            'originplace'], params['destinationplace'], params['outbounddate']]

        if params.get('inbounddate', None):
            params_list.append(params.get('inbounddate', None))

        params_path = '/'.join(params_list)

        return params_path

    def get_cheapest_price_by_date(self, **params):
        """
        {API_HOST}/apiservices/browsedates/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_DATES_SERVICE_URL,
            params_path=self.construct_params(params)
        )

        return self.make_request(service_url, **params)

    def get_cheapest_price_by_route(self, **params):
        """
        {API_HOST}/apiservices/browseroutes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_ROUTES_SERVICE_URL,
            params_path=self.construct_params(params)

        )
        return self.make_request(service_url, **params)

    def get_cheapest_quotes(self, **params):
        """
        {API_HOST}/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_QUOTES_SERVICE_URL,
            params_path=self.construct_params(params)
        )
        return self.make_request(service_url, **params)

    def get_grid_prices_by_date(self, **params):
        """
        {API_HOST}/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_GRID_SERVICE_URL,
            params_path=self.construct_params(params)
        )
        return self.make_request(service_url, **params)


class CarHire(Transport):

    """
    Carhire Live Pricing
    {API_HOST}/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/carhire/liveprices/v2'.format(api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_URL = '{api_host}/apiservices/hotels/autosuggest/v2'.format(api_host=Transport.API_HOST)

    def __init__(self, api_key):
        Transport.__init__(self, api_key)

    def location_autosuggest(self, **params):
        """
        http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2/{market}/{currency}/{locale}/{query}?apikey={apikey}
        """
        service_url = "{url}/{market}/{currency}/{locale}/{query}".format(
            url=self.LOCATION_AUTOSUGGEST_URL,
            market=params['market'],
            currency=params['currency'],
            locale=params['locale'],
            query=params['query']
        )
        return self.make_request(service_url, **params)

    def construct_params(self, params):
        """
        Construct params list in order
        """
        params_list = [params['market'], params['currency'], params['locale'], params['pickupplace'], params[
            'dropoffplace'], params['pickupdatetime'], params['dropoffdatetime'], params['driverage']]

        params_path = '/'.join(str(p) for p in params_list)

        return params_path

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-MM-DDThh:mm
        location: ISO code
        """

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self.construct_params(params)
        )

        poll_path = self.make_request(service_url,
                                      headers=self._default_session_headers(),
                                      callback=lambda resp: resp.headers['location'],
                                      userip=params['userip'])

        return "{url}{path}".format(url=self.API_HOST, path=poll_path)

    def is_poll_complete(self, poll_resp):
        if len(poll_resp['websites']) == 0:
            return False
        return all(not bool(website['in_progress']) for website in poll_resp['websites'])


class Hotels(Transport):

    """
    Hotels Live prices

    {API_HOST}/apiservices/hotels/liveprices/v2/{market}/{currency}/{locale}/{entityid}/{checkindate}/{checkoutdate}/{guests}/{rooms}?apiKey={apiKey}[&pageSize={pageSize}][&imageLimit={imageLimit}]
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/hotels/liveprices/v2'.format(api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_URL = '{api_host}/apiservices/hotels/autosuggest/v2'.format(api_host=Transport.API_HOST)

    def __init__(self, api_key):
        Transport.__init__(self, api_key)

    def location_autosuggest(self, **params):
        """
        {API_HOST}/apiservices/hotels/autosuggest/v2/{market}/{currency}/{locale}/{query}?apikey={apikey}
        """
        service_url = "{url}/{market}/{currency}/{locale}/{query}".format(
            url=self.LOCATION_AUTOSUGGEST_URL,
            market=params['market'],
            currency=params['currency'],
            locale=params['locale'],
            query=params['query']
        )
        return self.make_request(service_url, **params)

    def construct_params(self, params):
        """
        Construct params list in order
        """
        params_list = [params['market'], params['currency'], params['locale'], params['entityid'], params[
            'checkindate'], params['checkoutdate'], params['guests'], params['rooms']]

        params_path = '/'.join(str(p) for p in params_list)

        return params_path

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-MM-DDThh:mm
        location: ISO code
        """

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self.construct_params(params)
        )

        poll_path = self.make_request(service_url,
                                      headers=self._default_session_headers(),
                                      callback=lambda resp: resp.headers['location'])

        return "{url}{path}".format(url=self.API_HOST, path=poll_path)
