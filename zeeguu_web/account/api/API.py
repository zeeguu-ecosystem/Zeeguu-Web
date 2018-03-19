import flask
import requests
from zeeguu_web.account.api.api_exceptions import InvalidData, InvalidCredentials, NotFound, RequestError, ServerError
from zeeguu_web.app import configuration

possible_exceptions = [
    InvalidData,
    InvalidCredentials,
    NotFound,
    RequestError,
    ServerError
]

def _check_response(response):
    for ex in possible_exceptions:
        ex.shouldBeThrown(response)
    return response

def _api_path(path):
    zeeguu_path = configuration.get("ZEEGUU_API")
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
            _path = _api_path(path)
            resp = requests.get(_path, data=payload, params=params)
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise RequestError("Exception while performing request.")
    return _check_response(resp)

def post(path, payload={}, params={}, session_needed=False, session=None):
    return _api_call("post", path, payload, params, session_needed, session)


def get(path, payload={}, params={}, session_needed=False, session=None):
    return _api_call("get", path, payload, params, session_needed, session)
