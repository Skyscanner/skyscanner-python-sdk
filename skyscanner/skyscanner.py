# -*- coding: utf-8 -*-
import requests

class Transport():
    """
    Parent class for initialization
    """

    api_key = None

    MARKET_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/reference/v1.0/countries'
    LOCATION_AUTOSUGGEST_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0'

    def __init__(self, api_key):
        self.api_key = api_key

    def make_request(self, service_url, **params):
        """
        Reusable method for simple GET requests
        """
        params.update({
            'apiKey': self.api_key
        })

        r = requests.get(service_url, params=params)

        return r.json()

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
        Format: http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/{market}/{currency}/{locale}/?query={query}&apiKey={apiKey}        
        """

        url = "{url}/{market}/{currency}/{locale}/".format(url=self.LOCATION_AUTOSUGGEST_SERVICE_URL,
                                                           market=market, currency=currency, locale=locale)

        return self.make_request(url, query=query)

    def poll_session(self, poll_url, **params):
        """
        Poll the URL
        """
        r = requests.get(poll_url, params=params)

        return r.json()        


class Flights(Transport):

    """
    Flights Live Pricing
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList
    """

    PRICING_SESSION_URL = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'

    def __init__(self, api_key):
        Transport.__init__(self, api_key)

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-mm-dd
        location: ISO code
        """
        params.update({
            'apiKey': self.api_key
        })

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
        }

        r = requests.post(
            self.PRICING_SESSION_URL, data=params, headers=headers)

        headers = r.headers

        return headers['location']


    def request_booking_details(self, poll_url, **params):
        """
        Request for booking details
        URL Format: http://partners.api.skyscanner.net/apiservices/pricing/v1.0/{session key}/booking?apiKey={apiKey}
        """
        params.update({
            'apiKey': self.api_key
        })
        poll_url = "%s/booking" % poll_url

        r = requests.put(poll_url, params=params)

        print r

        headers = r.headers
        print r.url
        print poll_url
        print "headers: %s" % headers

        return headers['location']

    def get_result(self, **params):
        """
        Get all Itineraries, no filtering, etc.
        """
        print "params: %s" % params

        poll_url = self.create_session(**params)
        results = self.poll_session(poll_url, apiKey=self.api_key)

        return results


class FlightsCache(Flights):

    """
    Flights Browse Cache
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsBrowseCacheOverview
    """

    BROWSE_QUOTES_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0'
    BROWSE_ROUTES_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0'
    BROWSE_DATES_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/browsedates/v1.0'
    BROWSE_GRID_SERVICE_URL = 'http://partners.api.skyscanner.net/apiservices/browsegrid/v1.0'

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
        http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_DATES_SERVICE_URL,
            params_path=self.construct_params(params)
        )

        return self.make_request(service_url, **params)

    def get_cheapest_price_by_route(self, **params):
        """
        http://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_ROUTES_SERVICE_URL,
            params_path=self.construct_params(params)

        )
        return self.make_request(service_url, **params)

    def get_cheapest_quotes(self, **params):
        """
        http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_QUOTES_SERVICE_URL,
            params_path=self.construct_params(params)
        )
        return self.make_request(service_url, **params)

    def get_grid_prices_by_date(self, **params):
        """
        http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_GRID_SERVICE_URL,
            params_path=self.construct_params(params)
        )
        return self.make_request(service_url, **params)


class CarHire(Transport):

    """
    Carhire Live Pricing
    http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip} 

    """
    BASE_URL = 'http://partners.api.skyscanner.net'
    PRICING_SESSION_URL = 'http://partners.api.skyscanner.net/apiservices/carhire/liveprices/v2'
    LOCATION_AUTOSUGGEST_URL = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2'

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

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
        }

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self.construct_params(params)
        )

        params = {
            'apiKey': self.api_key,
            'userip': params['userip']
        }

        r = requests.get(
            service_url, params=params, headers=headers)

        print "r.url: %s" % r.url

        headers = r.headers

        print "headers: %s" % headers

        return headers['location']

    def get_result(self, **params):
        """
        Get all Itineraries, no filtering, etc.
        """
        print "params: %s" % params

        poll_path = self.create_session(**params)

        print "poll_path: %s" % poll_path

        poll_url = "{url}{path}".format(
            url=self.BASE_URL,
            path=poll_path
        )

        results = self.poll_session(poll_url)

        return results

class Hotels(Transport):
    """
    Hotels Live prices

    http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2/{market}/{currency}/{locale}/{entityid}/{checkindate}/{checkoutdate}/{guests}/{rooms}?apiKey={apiKey}[&pageSize={pageSize}][&imageLimit={imageLimit}]    
    """

    BASE_URL = 'http://partners.api.skyscanner.net'
    PRICING_SESSION_URL = 'http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2'
    LOCATION_AUTOSUGGEST_URL = 'http://partners.api.skyscanner.net/apiservices/hotels/autosuggest/v2'

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

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
        }

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self.construct_params(params)
        )

        params = {
            'apiKey': self.api_key
        }

        r = requests.get(
            service_url, params=params, headers=headers)

        print "r.url: %s" % r.url

        headers = r.headers

        print "headers: %s" % headers

        return headers['location']

    def get_result(self, **params):
        """
        Get all Itineraries, no filtering, etc.
        """
        print "params: %s" % params

        poll_path = self.create_session(**params)

        print "poll_path: %s" % poll_path

        poll_url = "{url}{path}".format(
            url=self.BASE_URL,
            path=poll_path
        )

        results = self.poll_session(poll_url)

        return results