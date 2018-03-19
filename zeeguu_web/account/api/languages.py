from flask import json

from zeeguu_web.account.api.API import get

api_available_languages = "available_languages"
api_available_native_languages = "available_native_languages"


def get_available_languages():
    resp = get(api_available_languages)
    _json = json.loads(resp.content)
    return _json


def get_available_native_languages():
    resp = get(api_available_native_languages)
    _json = json.loads(resp.content)
    return _json
