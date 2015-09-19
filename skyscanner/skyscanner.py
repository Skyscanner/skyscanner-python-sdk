# -*- coding: utf-8 -*-
import sys
import time
import logging
import requests
try:
    import lxml.etree as etree
except ImportError:
    import xml.etree.ElementTree as etree


def configure_logger(log_level=logging.WARN):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    try:
        sa = logging.StreamHandler(stream=sys.stdout)
    except TypeError:
        sa = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    sa.setFormatter(formatter)
    logger.addHandler(sa)
    return logger

log = configure_logger()
STRICT, GRACEFUL, IGNORE = 'strict', 'graceful', 'ignore'


class ExceededRetries(Exception):

    """Is thrown when allowed number of polls were performed but response is not complete yet."""
    pass


class EmptyResponse(Exception):

    """Is thrown when API returns empty response."""
    pass


class MissingParameter(KeyError):

    """Is thrown when expected request parameter is missing."""
    pass

class NotModified(Exception):

    """Is thrown when the server gives a 304 response."""
    pass

class Transport(object):

    """
    Parent class for initialization
    """
    API_HOST = 'http://partners.api.skyscanner.net'
    MARKET_SERVICE_URL = '{api_host}/apiservices/reference/v1.0/countries'.format(
        api_host=API_HOST)
    LOCATION_AUTOSUGGEST_URL = '{api_host}/apiservices/autosuggest/v1.0'.format(
        api_host=API_HOST)
    LOCATION_AUTOSUGGEST_PARAMS = ('market', 'currency', 'locale')
    _SUPPORTED_FORMATS = ('json', 'xml')

    def __init__(self, api_key, response_format='json'):
        """
        :param api_key - The API key to identify ourselves
        :param response_format - specify preferred format of the response, default is 'json'
        """
        if not api_key:
            raise ValueError('API key must be specified.')
        if response_format.lower() not in self._SUPPORTED_FORMATS:
            raise ValueError('Unknown response format: %s, supported formats are: %s' %
                             (response_format, ', '.join(self._SUPPORTED_FORMATS)))
        self.api_key = api_key
        self.response_format = response_format.lower()

    def get_result(self, errors=STRICT, **params):
        """
        Get all results, no filtering, etc. by creating and polling the session.
        """
        return self.poll_session(self.create_session(**params), errors=errors)

    def make_request(self, service_url, method='get', headers=None, data=None,
                     callback=None, errors=STRICT, **params):
        """
        Reusable method for performing requests.

        :param service_url - URL to request
        :param method - request method, default is 'get'
        :param headers - request headers
        :param data - post data
        :param callback - callback to be applied to response,
                          default callback will parse response as json object.
        :param errors - specifies communication errors handling mode, possible values are:
                         * strict (default) - throw an error as soon as one occurred
                         * graceful - ignore certain errors, e.g. EmptyResponse
                         * ignore - ignore all errors and return a result in any case.
                                    NOTE that it DOES NOT mean that no exceptions can be
                                    raised from this method, it mostly ignores communication
                                    related errors.
                         * None or empty string equals to default
        :param params - additional query parameters for request
        """
        error_modes = (STRICT, GRACEFUL, IGNORE)
        error_mode = errors or GRACEFUL
        if error_mode.lower() not in error_modes:
            raise ValueError(
                'Possible values for errors argument are: %s' % ', '.join(error_modes))

        if callback is None:
            callback = self._default_resp_callback

        if 'apikey' not in service_url.lower():
            params.update({
                'apiKey': self.api_key
            })

        request = getattr(requests, method.lower())
        log.debug('* Request URL: %s' % service_url)
        log.debug('* Request method: %s' % method)
        log.debug('* Request query params: %s' % params)
        log.debug('* Request headers: %s' % headers)
        r = request(service_url, headers=headers, data=data, params=params)

        try:
            r.raise_for_status()
            return callback(r)
        except Exception as e:
            return self._with_error_handling(r, e, error_mode, self.response_format)

    def get_markets(self, market):
        """
        Get the list of markets
        http://business.skyscanner.net/portal/en-GB/Documentation/Markets
        """
        url = "{url}/{market}".format(url=self.MARKET_SERVICE_URL,
                                      market=market)
        return self.make_request(url, headers=self._headers())

    def location_autosuggest(self, **params):
        """
        Location Autosuggest Services
        Doc URLs: http://business.skyscanner.net/portal/en-GB/Documentation/Autosuggest
                  http://business.skyscanner.net/portal/en-GB/Documentation/CarHireAutoSuggest
                  http://business.skyscanner.net/portal/en-GB/Documentation/HotelsAutoSuggest
        Format: Generic -        {LOCATION_AUTOSUGGEST_URL}/{market}/{currency}/{locale}/?query={query}&apiKey={apiKey}
                CarHire/Hotels - {LOCATION_AUTOSUGGEST_URL}/{market}/{currency}/{locale}/{query}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.LOCATION_AUTOSUGGEST_URL,
            params_path=self._construct_params(
                params, self.LOCATION_AUTOSUGGEST_PARAMS)
        )
        return self.make_request(service_url, headers=self._headers(), **params)

    def create_session(self, **params):
        """Creates a session for polling. Should be implemented by sub-classes"""
        raise NotImplementedError('Should be implemented by a sub-class.')

    def poll_session(self, poll_url, initial_delay=2, delay=1, tries=20, errors=STRICT, **params):
        """
        Poll the URL
        :param poll_url - URL to poll, should be returned by 'create_session' call
        :param initial_delay - specifies how many seconds to wait before the first poll
        :param delay - specifies how many seconds to wait between the polls
        :param tries - number of polls to perform
        :param errors - errors handling mode, see corresponding parameter in 'make_request' method
        :param params - additional query params for each poll request
        """
        time.sleep(initial_delay)
        poll_response = None
        for n in range(tries):
            try:
                poll_response = self.make_request(poll_url, headers=self._headers(),
                                                  errors=errors, **params)

                if self.is_poll_complete(poll_response):
                    return poll_response

            except NotModified:
                pass
            time.sleep(delay)
               

        if STRICT == errors:
            raise ExceededRetries(
                "Failed to poll within {0} tries.".format(tries))
        else:
            return poll_response

    def is_poll_complete(self, poll_resp):
        """
        Checks the condition in poll response to determine if it is complete
        and no subsequent poll requests should be done.
        """
        if poll_resp.parsed is None:
            return False
        success_list = ['UpdatesComplete', True, 'COMPLETE']
        status = None
        if self.response_format == 'xml':
            status = poll_resp.parsed.find('./Status').text
        elif self.response_format == 'json':
            status = poll_resp.parsed.get(
                'Status', poll_resp.parsed.get('status'))
        if status is None:
            raise RuntimeError('Unable to get poll response status.')
        return status in success_list

    @staticmethod
    def _with_error_handling(resp, error, mode, response_format):

        def safe_parse(r):
            try:
                return Transport._parse_resp(r, response_format)
            except (ValueError, SyntaxError) as ex:
                log.error(ex)
                r.parsed = None
                return r

        if isinstance(error, requests.HTTPError):
            if resp.status_code == 400:
                # It means that request parameters were rejected by the server,
                # so we need to enrich standard error message with 'ValidationErrors'
                # from the response
                resp = safe_parse(resp)
                if resp.parsed is not None:
                    parsed_resp = resp.parsed
                    messages = []
                    if response_format == 'xml' and parsed_resp.find('./ValidationErrors') is not None:
                        messages = [e.find('./Message').text
                                    for e in parsed_resp.findall('./ValidationErrors/ValidationErrorDto')]
                    elif response_format == 'json' and 'ValidationErrors' in parsed_resp:
                        messages = [e['Message']
                                    for e in parsed_resp['ValidationErrors']]
                    error = requests.HTTPError(
                        '%s: %s' % (error, '\n\t'.join(messages)), response=resp)
            elif resp.status_code == 429:
                error = requests.HTTPError('%sToo many requests in the last minute.' % error,
                                           response=resp)

        if STRICT == mode:
            raise error
        elif GRACEFUL == mode:
            if isinstance(error, EmptyResponse):
                # Empty response is returned by the API occasionally,
                # in this case it makes sense to ignore it and retry.
                log.warning(error)
                resp.parsed = None
                return resp

            elif isinstance(error, requests.HTTPError):
                # Ignoring 'Too many requests' error,
                # since subsequent retries will come after a delay.
                if resp.status_code == 429:    # Too many requests
                    log.warning(error)
                    return safe_parse(resp)
                else:
                    raise error
            else:
                raise error
        else:
            # ignore everything, just log it and return whatever response we
            # have
            log.error(error)
            return safe_parse(resp)

    def _session_headers(self):
        headers = self._headers()
        headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        return headers

    def _headers(self):
        return {'Accept': 'application/%s' % self.response_format}

    def _default_resp_callback(self, resp):
        if resp.status_code == 304:
            raise NotModified
            
        if not resp or not resp.content:
            raise EmptyResponse('Response has no content.')

        try:
            parsed_resp = self._parse_resp(resp, self.response_format)
        except (ValueError, SyntaxError):
            raise ValueError('Invalid %s in response: %s...' %
                             (self.response_format.upper(), resp.content[:100]))

        return parsed_resp

    @staticmethod
    def _construct_params(params, required_keys, opt_keys=None):
        """
        Construct params list in order of given keys.
        """
        try:
            params_list = [params.pop(key) for key in required_keys]
        except KeyError as e:
            raise MissingParameter(
                'Missing expected request parameter: %s' % e)
        if opt_keys:
            params_list.extend([params.pop(key)
                                for key in opt_keys if key in params])
        return '/'.join(str(p) for p in params_list)

    @staticmethod
    def _parse_resp(resp, response_format):
        resp.parsed = etree.fromstring(
            resp.content) if response_format == 'xml' else resp.json()
        return resp


class Flights(Transport):

    """
    Flights Live Pricing
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsLivePricingList
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/pricing/v1.0'.format(
        api_host=Transport.API_HOST)

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-mm-dd
        location: ISO code
        """
        return self.make_request(self.PRICING_SESSION_URL,
                                 method='post',
                                 headers=self._session_headers(),
                                 callback=lambda resp: resp.headers[
                                     'location'],
                                 data=params)

    def request_booking_details(self, poll_url, **params):
        """
        Request for booking details
        URL Format: {API_HOST}/apiservices/pricing/v1.0/{session key}/booking?apiKey={apiKey}
        """
        return self.make_request("%s/booking" % poll_url,
                                 method='put',
                                 headers=self._headers(),
                                 callback=lambda resp: resp.headers[
                                     'location'],
                                 **params)


class FlightsCache(Flights):

    """
    Flights Browse Cache
    http://business.skyscanner.net/portal/en-GB/Documentation/FlightsBrowseCacheOverview
    """

    BROWSE_QUOTES_SERVICE_URL = '{api_host}/apiservices/browsequotes/v1.0'.format(
        api_host=Transport.API_HOST)
    BROWSE_ROUTES_SERVICE_URL = '{api_host}/apiservices/browseroutes/v1.0'.format(
        api_host=Transport.API_HOST)
    BROWSE_DATES_SERVICE_URL = '{api_host}/apiservices/browsedates/v1.0'.format(
        api_host=Transport.API_HOST)
    BROWSE_GRID_SERVICE_URL = '{api_host}/apiservices/browsegrid/v1.0'.format(
        api_host=Transport.API_HOST)
    _REQ_PARAMS = ('market', 'currency', 'locale',
                   'originplace', 'destinationplace', 'outbounddate')
    _OPT_PARAMS = ('inbounddate',)

    def get_cheapest_price_by_date(self, **params):
        """
        {API_HOST}/apiservices/browsedates/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_DATES_SERVICE_URL,
            params_path=self._construct_params(
                params, self._REQ_PARAMS, self._OPT_PARAMS)
        )

        return self.make_request(service_url, headers=self._headers(), **params)

    def get_cheapest_price_by_route(self, **params):
        """
        {API_HOST}/apiservices/browseroutes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_ROUTES_SERVICE_URL,
            params_path=self._construct_params(
                params, self._REQ_PARAMS, self._OPT_PARAMS)

        )
        return self.make_request(service_url, headers=self._headers(), **params)

    def get_cheapest_quotes(self, **params):
        """
        {API_HOST}/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_QUOTES_SERVICE_URL,
            params_path=self._construct_params(
                params, self._REQ_PARAMS, self._OPT_PARAMS)
        )
        return self.make_request(service_url, headers=self._headers(), **params)

    def get_grid_prices_by_date(self, **params):
        """
        {API_HOST}/apiservices/browsequotes/v1.0/{market}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}
        """
        service_url = "{url}/{params_path}".format(
            url=self.BROWSE_GRID_SERVICE_URL,
            params_path=self._construct_params(
                params, self._REQ_PARAMS, self._OPT_PARAMS)
        )
        return self.make_request(service_url, headers=self._headers(), **params)


class CarHire(Transport):

    """
    Carhire Live Pricing
    {API_HOST}/apiservices/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}?apiKey={apiKey}&userip={userip}
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/carhire/liveprices/v2'.format(
        api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_URL = '{api_host}/apiservices/hotels/autosuggest/v2'.format(
        api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_PARAMS = ('market', 'currency', 'locale', 'query')

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-MM-DDThh:mm
        location: ISO code
        """

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self._construct_params(params, ('market', 'currency', 'locale',
                                                        'pickupplace', 'dropoffplace',
                                                        'pickupdatetime', 'dropoffdatetime',
                                                        'driverage'))
        )

        poll_path = self.make_request(service_url,
                                      headers=self._session_headers(),
                                      callback=lambda resp: resp.headers[
                                          'location'],
                                      userip=params['userip'])

        return "{url}{path}".format(url=self.API_HOST, path=poll_path)

    def is_poll_complete(self, poll_resp):
        if poll_resp.parsed is None:
            return False
        websites = None
        if self.response_format == 'xml':
            websites = poll_resp.parsed.findall('./Websites/WebsiteDto')
        elif self.response_format == 'json':
            websites = poll_resp.parsed['websites']
        if len(websites) == 0:
            return False
        return all(not bool(w.get('in_progress')) for w in websites)


class Hotels(Transport):

    """
    Hotels Live prices

    {API_HOST}/apiservices/hotels/liveprices/v2/{market}/{currency}/{locale}/{entityid}/{checkindate}/{checkoutdate}/{guests}/{rooms}?apiKey={apiKey}[&pageSize={pageSize}][&imageLimit={imageLimit}]
    """

    PRICING_SESSION_URL = '{api_host}/apiservices/hotels/liveprices/v2'.format(
        api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_URL = '{api_host}/apiservices/hotels/autosuggest/v2'.format(
        api_host=Transport.API_HOST)
    LOCATION_AUTOSUGGEST_PARAMS = ('market', 'currency', 'locale', 'query')

    def create_session(self, **params):
        """
        Create the session
        date format: YYYY-MM-DDThh:mm
        location: ISO code
        """

        service_url = "{url}/{params_path}".format(
            url=self.PRICING_SESSION_URL,
            params_path=self._construct_params(params, ('market', 'currency', 'locale',
                                                        'entityid', 'checkindate', 'checkoutdate',
                                                        'guests', 'rooms'))
        )

        poll_path = self.make_request(service_url,
                                      headers=self._session_headers(),
                                      callback=lambda resp: resp.headers['location'])

        return "{url}{path}".format(url=self.API_HOST, path=poll_path)
