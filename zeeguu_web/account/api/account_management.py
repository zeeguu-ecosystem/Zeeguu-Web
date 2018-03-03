import flask
import requests
import zeeguu

from zeeguu_web.account.api.API import post

api_create_user = "add_user/"
api_native = "native_language/"
api_learned = "learned_language/"


def create_account(email, username, password, learning_language, native_language):
    api_address = api_create_user + email
    resp = post(api_address, payload={"password": password, "username": username})
    session = int(resp.text)
    # What to do when the server crashes here?
    native = api_native + native_language.code
    learned = api_learned + learning_language.code
    resp = post(native, session_needed=True, session=session)
    resp = post(learned, session_needed=True, session=session)
    return session
