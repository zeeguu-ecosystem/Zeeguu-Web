from abc import abstractmethod

from flask import json


def message(response):
    try:
        data = json.loads(response.text)
        return data["message"]
    except Exception:
        return ""

class ServerException(Exception):
    def __init__(self, message):
        super()
        self.message = message

    @classmethod
    @abstractmethod
    def shouldBeThrown(cls, response):
        pass


class InvalidData(ServerException):
    @classmethod
    def shouldBeThrown(cls, response):
        if response.status_code == 400:
            raise InvalidData(message(response))

class InvalidCredentials(ServerException):
    @classmethod
    def shouldBeThrown(cls, response):
        if response.status_code == 401:
            raise InvalidCredentials(message(response))

class NotFound(ServerException):
    @classmethod
    def shouldBeThrown(cls, response):
        if response.status_code == 404:
            raise NotFound(message(response))

class RequestError(ServerException):
    @classmethod
    def shouldBeThrown(cls, response):
        if response.status_code == 430:
            raise RequestError(message(response))

class ServerError(ServerException):
    @classmethod
    def shouldBeThrown(cls, response):
        if response.status_code == 530:
            raise ServerError(message(response))