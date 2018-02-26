import flask
import requests
import zeeguu

from zeeguu_web.account.api import retrievePayload


class SessionManagement:

    api_login = zeeguu.app.config.get("ZEEGUU_API") + "/session/"
    api_logout = zeeguu.app.config.get("ZEEGUU_API") + "/logout_session"
    api_validate = zeeguu.app.config.get("ZEEGUU_API") + "/validate"

    @classmethod
    def login(cls, email, password):
        api_address = cls.api_login + email
        resp = requests.post(api_address, data = {"password": password})
        payload = retrievePayload(resp)
        return payload.text

    @classmethod
    def logout(cls):
        session_id = flask.session["session_id"]
        resp = requests.get(cls.api_logout, params={"session": session_id})
        retrievePayload(resp)
        return True

    @classmethod
    def validate(cls):
        session_id = flask.session["session_id"]
        resp = requests.get(cls.api_validate, params={"session": session_id})
        payload = retrievePayload(resp)
        return True


