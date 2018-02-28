import flask
import requests
import zeeguu

from zeeguu_web.account.api import API_GET, API_POST


class SessionManagement:

    api_login = "session/"
    api_logout = "logout_session"
    api_validate = "validate"

    @classmethod
    def login(cls, email, password):
        url = cls.api_login + email
        resp = API_POST(url, payload={"password": password})
        return resp.text

    @classmethod
    def logout(cls):
        API_GET(cls.api_logout, session_needed=True)

    @classmethod
    def validate(cls):
        API_GET(cls.api_validate, session_needed=True)


