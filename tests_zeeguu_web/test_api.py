import pytest
import requests
from zeeguu_web.api_communication import api_connection
from zeeguu_web.api_communication.api_connection import APIException


class TestAPIConnection:

    def test_response_code_200(self):
        response = requests.Response()
        response.status_code = 200
        api_connection._check_response(response)   # No error should be throw, allowing the test to succeed.

    def test_response_code_above_400_throws_exception(self):
        response = requests.Response()
        response.status_code = 401
        with pytest.raises(APIException):
            api_connection._check_response(response)