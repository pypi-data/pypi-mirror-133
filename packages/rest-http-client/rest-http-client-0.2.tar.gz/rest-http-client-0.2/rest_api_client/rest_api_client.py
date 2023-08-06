import json
import logging
from time import sleep

import requests
import urllib3
from .modules import pretty_dict
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from logger_config import configure_logging

logger_name = 'http_logger'
configure_logging(logger_name)
logger = logging.getLogger(logger_name)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpClient:
    """Session class with response handling"""
    def __init__(self, address: str, prefix=None, **kwargs):
        logger.debug('Create new session, {}'.format(self))
        self.session = requests.Session()
        self.address = address
        self.prefix = prefix

        self.session.proxies = kwargs.get('proxies') or {'http': None, 'https': None}
        self.session.trust_env = False
        self.session.verify = False
        self.session.auth = kwargs.pop('auth', None)
        self.session.timeout = kwargs.pop('timeout', (10, 15))  # 10 sec for connection and 15 sec for reading

        self.set_token(kwargs.pop('token', None))

        self.session.headers["Content-Type"] = "application/json"
        self.request = self.session.request

        retries = Retry(redirect=5, backoff_factor=0.3, status_forcelist=[503])

        # for load test. Default 150
        adapter = HTTPAdapter(pool_connections=1000, pool_maxsize=1000, max_retries=retries)

        self.mount(adapter)
        assert not kwargs, 'Unknown params. {}'.format(kwargs)

    def __enter__(self):
        self.session = requests.Session()

    def mount(self, adapter: HTTPAdapter):
        self.session.mount(f'http://', adapter)
        self.session.mount(f'https://', adapter)

    def set_token(self, token, method='Bearer'):
        if token:
            token = {"Authorization": "{} {}".format(method, token)}
            self.session.headers.update(token)

    def add_headers(self, headers):
        self.session.headers.update(headers)

    @property
    def base_url(self):
        if self.prefix and self.prefix not in self.address:
            self.address += '/' + self.prefix
        return self.address

    def _request(self, http_method, relative_url, **kwargs):

        str_kwargs = {k: str(kwargs[k])[:100] for k in kwargs}

        assert relative_url.startswith('/')

        response = None  # When key interrupted script go to finally bellow and will raise error
        url = self.base_url + relative_url
        msg = '{} {} {}'.format(http_method, url, str_kwargs)
        logger.debug(msg)

        try:
            sleep(0.1)  # Several servers do not time to response simultaneously because add sleep
            response = self.request(http_method, url, **kwargs)

        except Exception as ex:
            logger.error('{}\nError message: {}'.format(msg, ex))
            response = getattr(ex, 'response')
            raise

        finally:
            self._check_for_error(response)
            return response

    @staticmethod
    def _check_for_error(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                body = response.json()
            except ValueError:
                body = {}

            try:
                request_body = json.loads(response.request.body)
            except json.decoder.JSONDecodeError:
                request_body = {}

            msg = f'\n***Request*** \n\n' \
                  f'{response.status_code} {response.request.method} {response.url} \n' \
                  f'Body: {pretty_dict(request_body)}\n' \
                  f'Headers: {pretty_dict(dict(response.request.headers))}\n' \
                  f'\n***Response*** \n\n' \
                  f'Headers: {pretty_dict(dict(response.headers))}\n' \
                  f'Text: {response.text}\n' \
                  f'JSON: {pretty_dict(body)}\n'
            logger.error(msg)

    def get(self, relative_url, **kwargs):
        return self._request('GET', relative_url, **kwargs)

    def post(self, relative_url, **kwargs):
        return self._request('POST', relative_url, **kwargs)

    def put(self, relative_url, **kwargs):
        return self._request('PUT', relative_url, **kwargs)

    def delete(self, relative_url, **kwargs):
        return self._request('DELETE', relative_url, **kwargs)

    def patch(self, relative_url, **kwargs):
        return self._request('PATCH', relative_url, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def close(self):
        self.session.close()
        logger.debug('Session has been closed')
