from abc import abstractmethod


class ServerException(Exception):
    def __init__(self, message):
        super()
        self.message = message

    @classmethod
    @abstractmethod
    def shouldBeThrown(cls, response):
        pass


class InvalidData(ServerException):
    def shouldBeThrown(cls, response):
        if response.code == 401:
            raise InvalidData(response.data)

class InvalidCredentials(ServerException):
    def shouldBeThrown(cls, response):
        if response.code == 400:
            raise InvalidCredentials(response.data)

class NotFound(ServerException):
    def shouldBeThrown(cls, response):
        if response.code == 404:
            raise NotFound(response.data)

class RequestError(ServerException):
    def shouldBeThrown(cls, response):
        if response.code == 430:
            raise RequestError(response.data)

class ServerError(ServerException):
    def shouldBeThrown(cls, response):
        if response.code == 530:
            raise ServerError(response.data)

