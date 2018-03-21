import datetime
from flask import json

from zeeguu_web.account.api.api_connection import post
from zeeguu_web.account.api.models.Bookmark import Bookmark

api_bookmarks_by_date = "bookmarks_by_day"

def get_bookmarks_by_date(date):
    _date_string = date.strftime('%Y-%m-%dT%H:%M:%S')
    _payload = {
        "with_context" : True,
        "after_date" : _date_string
    }
    resp = post(api_bookmarks_by_date, payload=_payload, session_needed=True)
    _json = json.loads(resp.content)
    # ("bookmarks.html",
    #  bookmarks_by_url=bookmarks_by_url,
    # urls_by_date=urls_by_date,
    # sorted_dates=most_recent_seven_days,
    # bookmark_counts_by_date=bookmark_counts_by_date,
    # user=flask.g.user)

    sorted_dates = []
    bookmarks_by_url = {}
    urls_by_date = {}
    bookmark_counts_by_date = {}

    for data in _json:
        d = datetime.datetime.strptime(data["date"], "%A, %d %B %Y")
        sorted_dates.append(d)
        for bm_json in data["bookmarks"]:
            bm = Bookmark.from_json(bm_json)
            bm.set_date(d)
            urls_by_date.setdefault(d, set()).add(bm.url)
            bookmarks_by_url.setdefault(bm.url, []).append(bm)

        bookmark_counts_by_date.setdefault(d, set()).add(len(data["bookmarks"]))

    return {
        "sorted_dates" : sorted_dates,
        "bookmarks_by_url" : bookmarks_by_url,
        "urls_by_date" : urls_by_date,
        "bookmark_counts_by_date" : bookmark_counts_by_date
    }