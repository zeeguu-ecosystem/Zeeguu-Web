import json

from zeeguu_web.api_communication.api_connection import get, post

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


def user_details(session_id: int):
    resp = get(USER_DETAILS + "?session=" + str(session_id), session_needed=False)
    return json.loads(resp.text)
