import flask
import requests
import zeeguu


class AccountManagement:

    api_create_user = zeeguu.app.config.get("ZEEGUU_API") + "/add_user/"

    @classmethod
    def create_account(cls, email, password, learning_language, native_language):
        api_address = cls.api_login + email
        resp = requests.post(api_address, data = {"password": password})
        if resp.status_code is not 200:
            return -1
        else:
            return int(resp.text)


