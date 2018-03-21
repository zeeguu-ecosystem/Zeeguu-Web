import pytest
import requests
from flask import jsonify

from zeeguu_web.account.api import API
from zeeguu_web.account.api.API import ServerException


class TestAPI:

    def test_response_code_200(self):
        response = requests.Response()
        response.status_code = 200
        API._check_response(response)   # No error should be throw, allowing the test to succeed.

    def test_response_code_above_400_throws_exception(self):
        response = requests.Response()
        response.status_code = 401
        with pytest.raises(ServerException):
            API._check_response(response)