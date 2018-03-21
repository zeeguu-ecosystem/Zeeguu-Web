from zeeguu_web.account.api.api_connection import get, post

LOGIN = "session/"
LOGOUT = "logout_session"
VALIDATE = "validate"

def login(email, password):
    url = LOGIN + email
    resp = post(url, payload={"password": password})
    return resp.text

def logout():
    get(LOGOUT, session_needed=True)

def validate(cls):
    get(VALIDATE, session_needed=True)
