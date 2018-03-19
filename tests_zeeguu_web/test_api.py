import pytest
import requests
from flask import json, jsonify

from zeeguu_web.account.api import API
from zeeguu_web.account.api.api_exceptions import InvalidData, ServerException, InvalidCredentials, NotFound, \
    RequestError, ServerError


class TestAPI:

    def test_response_code_200(self):
        response = requests.Response()
        response.status_code = 200
        API._check_response(response)   # No error should be throw, allowing the test to succeed.

    def test_response_InvalidData(self):
        response = requests.Response()
        response.status_code = 400
        with pytest.raises(InvalidData):
            API._check_response(response)

    def test_response_InvalidCredentials(self):
        response = requests.Response()
        response.status_code = 401
        with pytest.raises(InvalidCredentials):
            API._check_response(response)

    def test_response_NotFound(self):
        response = requests.Response()
        response.status_code = 404
        with pytest.raises(NotFound):
            API._check_response(response)

    def test_response_RequestError(self):
        response = requests.Response()
        response.status_code = 430
        with pytest.raises(RequestError):
            API._check_response(response)

    def test_response_ServerError(self):
        response = requests.Response()
        response.status_code = 530
        with pytest.raises(ServerError):
            API._check_response(response)

