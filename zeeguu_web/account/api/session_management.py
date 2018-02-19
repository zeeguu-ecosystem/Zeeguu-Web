import flask
import requests
import zeeguu


class SessionManagement:

    api_login = zeeguu.app.config.get("ZEEGUU_API") + "/session/"
    api_logout = zeeguu.app.config.get("ZEEGUU_API") + "/logout_session"
    api_validate = zeeguu.app.config.get("ZEEGUU_API") + "/validate"

    @classmethod
    def login(cls, email, password):
        api_address = cls.api_login + email
        resp = requests.post(api_address, data = {"password": password})
        if resp.status_code is not 200:
            return -1
        else:
            return int(resp.text)

    @classmethod
    def logout(cls):
        session_id = flask.session["session_id"]
        resp = requests.get(cls.api_logout, params={"session": session_id})
        if resp.status_code is not 200:
            return True
        else:
            return False

    @classmethod
    def validate(cls):
        session_id = flask.session["session_id"]
        resp = requests.get(cls.api_validate, params={"session": session_id})
        if resp.status_code is not 200:
            return True
        else:
            return False


