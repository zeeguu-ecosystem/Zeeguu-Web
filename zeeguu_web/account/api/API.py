import flask
import requests
import zeeguu

from zeeguu_web.account.api.api_exceptions import APIConnectionError


def _check_response(response):
    if response.status_code is 200:
        return response
    else:
        raise APIConnectionError(response.status_code)


def _api_path(path):
    zeeguu_path = zeeguu.app.config.get("ZEEGUU_API")
    if zeeguu_path.endswith("/"):
        return zeeguu_path + path
    return zeeguu_path + "/" + path

def _api_call(function, path, payload={}, params={}, session_needed=False, session=None):
    if session_needed:
        if session is None:
            session_id = flask.session["session_id"]
        else:
            session_id = session
        params["session"] = session_id
    try:
        if function == "post":
            resp = requests.post(_api_path(path), data=payload, params=params)
        else:
            resp = requests.get(_api_path(path), data=payload, params=params)
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise APIConnectionError(404)
    return _check_response(resp)

def post(path, payload={}, params={}, session_needed=False, session=None):
    _api_call("post", path, payload, params, session_needed, session)


def get(path, payload={}, params={}, session_needed=False, session=None):
    _api_call("get", path, payload, params, session_needed, session)
