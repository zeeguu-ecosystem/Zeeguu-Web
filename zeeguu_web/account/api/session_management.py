from zeeguu_web.account.api.API import get, post

api_login = "session/"
api_logout = "logout_session"
api_validate = "validate"

def login(email, password):
    url = api_login + email
    resp = post(url, payload={"password": password})
    return resp.text

def logout():
    get(api_logout, session_needed=True)

def validate(cls):
    get(api_validate, session_needed=True)
