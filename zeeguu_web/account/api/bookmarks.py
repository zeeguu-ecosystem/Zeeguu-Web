from flask import json

from zeeguu_web.account.api.API import get, post

api_bookmarks_by_date = "bookmarks_by_day"


def get_bookmarks_by_date(date):
    _date_string = date.strftime('%Y-%m-%dT%H:%M:%S')
    _payload = {
        "with_context" : True,
        "after_date" : _date_string
    }
    resp = post(api_bookmarks_by_date, payload=_payload, session_needed=True)
    _json = json.loads(resp.content)
    return _json