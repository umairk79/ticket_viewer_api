import unittest
from unittest import mock
from tickets.views import Tickets
from requests.models import Response
import json
from requests.exceptions import Timeout, TooManyRedirects, RequestException


# Mock Request Class
class Request:
    def __init__(self, json_data):
        self.data = json_data


# This method will be used by the mock to replace requests.get
def mocked_requests_get_success(*args, **kwargs):
    response = Response()
    response.status_code = 200
    with open('tickets/static/test/resp200.json') as json_file:
        response_json = json.load(json_file)
    response._content = json.dumps(response_json).encode('utf-8')
    return response


# Main Test Class
class Test(unittest.TestCase):

    tickets = Tickets()
    request = Request({'data': {'email': 'a@b.com', 'password': 'xxx', 'subdomain': 'xxx', 'page': 2}})

    # happy path scenario test
    @mock.patch('tickets.views.requests.get', side_effect=mocked_requests_get_success)
    def test_connect(self, mock_get):

        json_data = self.tickets.post(self.request)
        self.assertEqual(len(json_data.data['tickets']), 1)
        self.assertEqual(json_data.status_code, 200)

    # Timeout scenario test
    @mock.patch('tickets.views.requests.get', side_effect=Timeout())
    def test_connect_timeout(self, mock_get):
        json_data = self.tickets.post(self.request)
        self.assertEqual(json_data.data['error'], "Timeout while trying to connect with Zendesk")
        self.assertEqual(json_data.status_code, 500)

    # Too many redirects scenario test
    @mock.patch('tickets.views.requests.get', side_effect=TooManyRedirects())
    def test_connect_too_many_redirects(self, mock_get):
        json_data = self.tickets.post(self.request)
        self.assertEqual(json_data.data['error'], "Bad Zendesk URL - Too Many Redirects")
        self.assertEqual(json_data.status_code, 500)

    # Other api scenation such as 401/403/404 etc test
    @mock.patch('tickets.views.requests.get', side_effect=RequestException())
    def test_connect_request_exception(self, mock_get):
        json_data = self.tickets.post(self.request)
        self.assertIsNotNone(json_data.data['error'])
        self.assertEqual(json_data.status_code, 500)

    # General error scenario test
    @mock.patch('tickets.views.requests.get', side_effect=Exception())
    def test_connect_exception(self, mock_get):
        json_data = self.tickets.post(self.request)
        self.assertIsNotNone(json_data.data['error'])
        self.assertEqual(json_data.status_code, 500)

