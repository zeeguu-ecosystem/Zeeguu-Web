import flask
import requests
import zeeguu

from zeeguu_web.account.api.API import API


class SessionManagement:

    api_login = "session/"
    api_logout = "logout_session"
    api_validate = "validate"

    @classmethod
    def login(cls, email, password):
        url = cls.api_login + email
        resp = API.post(url, payload={"password": password})
        return resp.text

    @classmethod
    def logout(cls):
        API.get(cls.api_logout, session_needed=True)

    @classmethod
    def validate(cls):
        API.get(cls.api_validate, session_needed=True)


