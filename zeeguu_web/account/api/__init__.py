import flask
import requests
import zeeguu


class APIConnectionError(Exception):
    def __init__(self, code):
        super()
        self.status_code = code


def __check_response(response):
    if response.status_code is 200:
        return response
    else:
        raise APIConnectionError(response.status_code)


def api_path(path):
    return zeeguu.app.config.get("ZEEGUU_API") + "/" + path


def API_POST(path, payload={}, params={}, session_needed=False, session=None):
    if session_needed:
        if session is None:
            session_id = flask.session["session_id"]
        else:
            session_id = session
        params["session"] = session_id
    try:
        resp = requests.post(api_path(path), data=payload, params=params)
    except ConnectionError:
        raise APIConnectionError(404)
    return __check_response(resp)


def API_GET(path, payload={}, params={}, session_needed=False, session=None):
    if session_needed:
        if session is None:
            session_id = flask.session["session_id"]
        else:
            session_id = session
        params["session"] = session_id
    try:
        resp = requests.get(api_path(path), data=payload, params=params)
    except ConnectionError:
        raise APIConnectionError(404)
    return __check_response(resp)
