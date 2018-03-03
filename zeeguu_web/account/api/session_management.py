import flask
import requests
import zeeguu

from zeeguu_web.account.api.API import get, post

api_login = "session/"
api_logout = "logout_session"
api_validate = "validate"

def login(cls, email, password):
    url = cls.api_login + email
    resp = post(url, payload={"password": password})
    return resp.text

def logout(cls):
    get(cls.api_logout, session_needed=True)

def validate(cls):
    get(cls.api_validate, session_needed=True)
