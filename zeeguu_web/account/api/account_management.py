import flask
import requests
import zeeguu

from zeeguu_web.account.api import API


class AccountManagement:

    api_create_user = "add_user/"
    api_native = "native_language/"
    api_learned = "learned_language/"

    @classmethod
    def create_account(cls, email, username, password, learning_language, native_language):
        api_address = cls.api_create_user + email
        resp = API.post(api_address, payload = {"password": password, "username":username})
        session = int(resp.text)
            # What to do when the server crashes here?
        native = cls.api_native + native_language.code
        learned = cls.api_learned + learning_language.code
        resp = API.post(native, session_needed=True, session=session)
        resp = API.post(learned, session_needed=True, session=session)
        return session
