from zeeguu_web.account.api.api_connection import post

CREATE_USER = "add_user/"
NATIVE_LANGUAGE = "native_language/"
LEARNED_LANGUAGE = "learned_language/"

REQUEST_CODE = "send_code/"
RESET_PASSWORD = "reset_password/"


def create_account(email, username, password, learning_language, native_language, invite_code):
    api_address = CREATE_USER + email
    resp = post(api_address, payload={"password": password, "username": username, "invite_code": invite_code})
    session = int(resp.text)

    # What to do when the server crashes here?
    native = NATIVE_LANGUAGE + native_language
    learned = LEARNED_LANGUAGE + learning_language
    resp = post(native, session_needed=True, session=session)
    resp = post(learned, session_needed=True, session=session)
    return session


def request_code(email):
    api_addres = REQUEST_CODE + email
    resp = post(api_addres)


def reset_password(code, email, password):
    api_address = RESET_PASSWORD + email
    resp = post(api_address, payload={"code": code, "password": password})
