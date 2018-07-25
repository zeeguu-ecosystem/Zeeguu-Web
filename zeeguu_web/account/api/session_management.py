import json

from zeeguu_web.account.api.api_connection import get, post

LOGIN = "session/"
LOGOUT = "logout_session"
VALIDATE = "validate"
USER_DETAILS = "get_user_details"


def login(email, password):
    url = LOGIN + email
    resp = post(url, payload={"password": password})
    return resp.text


def logout():
    get(LOGOUT, session_needed=True)


def validate():
    resp = get(VALIDATE, session_needed=True)
    return resp.text


def user_details(sessionID):
    resp = get(USER_DETAILS + "?session=" + sessionID, session_needed=False)
    return json.loads(resp.text)
