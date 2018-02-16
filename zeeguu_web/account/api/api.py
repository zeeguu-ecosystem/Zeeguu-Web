import requests
import zeeguu


class API:
    @classmethod
    def login(cls, email, password):
        api_address = zeeguu.app.config.get("ZEEGUU_API") + "/session/" + email
        resp = requests.post(api_address, {"password": password})
        if resp.status_code is not 200:
            return -1
        else:
            return int(resp.text)
