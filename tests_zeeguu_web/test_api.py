import pytest
import requests
from zeeguu_web.account.api import api_controller
from zeeguu_web.account.api.api_controller import APIException


class testAPIController:

    def test_response_code_200(self):
        response = requests.Response()
        response.status_code = 200
        api_controller._check_response(response)   # No error should be throw, allowing the test to succeed.

    def test_response_code_above_400_throws_exception(self):
        response = requests.Response()
        response.status_code = 401
        with pytest.raises(APIException):
            api_controller._check_response(response)