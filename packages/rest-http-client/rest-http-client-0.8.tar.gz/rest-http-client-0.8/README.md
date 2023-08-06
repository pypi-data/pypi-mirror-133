rest-http-client: Configurable and flexible http(s)-client for your python applications
============================================================================


Description
-----------

The **rest-http-client** package is a basic configurable rest api client. This package is currently tested on Python =< 2.7.
This  package worked on multithreding mode

Installation
------------

    pip install rest-http-client

or

download the `latest release` and run

    python setup.py install


Usage
-----
Example in folder **tests**. 

The first you can configure http or https client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import logging

from rest_api_client import HttpClient
from .testapis import TestAPIs

logger = logging.getLogger('http_logger')

class TestRestAPI(HttpClient):
    _WRAPPERS = [  # list of api clients
        TestAPIs
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.testapis = None

        for e in self._WRAPPERS:
            attr_name = e.__name__.lower()
            setattr(self, attr_name, e(self))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class **TestAPIs** where you list all api requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from http import HTTPStatus


class TestAPIs:
    def __init__(self, client):
        self.client = client
        self.client.add_headers({
            "Accept": "*/*",
            "Content-Type": "application/json",
        })

    def get_request(self):
        response = self.client.get('/echo')
        assert response.status_code == HTTPStatus.OK, 'Invalid request'
        return response

    def post_request(self, body: dict):
        response = self.client.post('/echo/post/form', json=body)
        assert response.status_code == HTTPStatus.OK, 'Invalid request'
        return response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then has to create object of **TestRestAPI** and use in tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from tests.api import TestRestAPI

client = TestRestAPI(address='https://reqbin.com')


def test_check_get_request():
    response = client.testapis.get_request()
    assert 'Simple echo interface for HTTP methods' in response.text, 'Something is wrong'


def test_check_post_request():
    body = {
        'key1': 'value1',
        'key2': 'value2',
    }
    response = client.testapis.post_request(body=body)
    assert 'Success' in response.text, 'Something is wrong'

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Console Output**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
============================= test session starts =============================
collecting ... collected 2 items

test_apis.py::test_check_get_request 
test_apis.py::test_check_post_request 

======================== 2 passed, 3 warnings in 0.75s ========================

Process finished with exit code 0
PASSED                              [ 50%]
PASSED                             [100%]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~