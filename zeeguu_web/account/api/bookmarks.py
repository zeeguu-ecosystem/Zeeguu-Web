import datetime
from flask import json

from zeeguu_web.account.api.api_connection import post
from zeeguu_web.account.api.models.Bookmark import Bookmark

BOOKMARKS_BY_DATE = "bookmarks_by_day"
DELETE_BOOKMARK = "delete_bookmark/"
STAR_BOOKMARK = "star_bookmark/"
UNSTAR_BOOKMARK = "unstar_bookmark/"

def get_bookmarks_by_date(date):
    _date_string = date.strftime('%Y-%m-%dT%H:%M:%S')
    _payload = {
        "with_context" : True,
        "after_date" : _date_string
    }
    resp = post(BOOKMARKS_BY_DATE, payload=_payload, session_needed=True)
    _json = json.loads(resp.content)

    sorted_dates = []
    bookmarks_by_url = {}
    urls_by_date = {}
    bookmark_counts_by_date = {}

    for data in _json:
        d = datetime.datetime.strptime(data["date"], "%A, %d %B %Y")
        sorted_dates.append(d)
        for bm_json in data["bookmarks"]:
            try :
                bm = Bookmark.from_json(bm_json)
                bm.set_date(d)
                urls_by_date.setdefault(d, set()).add(bm.url)
                bookmarks_by_url.setdefault(bm.url, []).append(bm)
            except Exception:
                print("Parsing bookmark failed")

        bookmark_counts_by_date.setdefault(d, set()).add(len(data["bookmarks"]))

    return {
        "sorted_dates" : sorted_dates,
        "bookmarks_by_url" : bookmarks_by_url,
        "urls_by_date" : urls_by_date,
        "bookmark_counts_by_date" : bookmark_counts_by_date
    }

def delete_bookmark(bookmark_id):
    path = DELETE_BOOKMARK + str(bookmark_id)
    resp = post(path)
    return resp.text

def star_bookmark(bookmark_id):
    path = STAR_BOOKMARK + str(bookmark_id)
    resp = post(path)
    return resp.text

def unstar_bookmark(bookmark_id):
    path = UNSTAR_BOOKMARK + str(bookmark_id)
    resp = post(path)
    return resp.text
