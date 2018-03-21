import datetime

from zeeguu_web.account.api.bookmarks import get_bookmarks_by_date, star_bookmark, unstar_bookmark, delete_bookmark
from . import account, login_first
import flask
from zeeguu.model import Bookmark, Text
import zeeguu


@account.route("/bookmarks")
@login_first
def bookmarks():

    d = datetime.datetime.now() - datetime.timedelta(days = 365)
    data = get_bookmarks_by_date(d)

    # bookmarks_list, dates = flask.g.user.bookmarks_by_date()
    #
    # most_recent_seven_days = dates[0:6]
    #
    # urls_by_date = {}
    # bookmarks_by_url = {}
    # for date in most_recent_seven_days:
    #     for bookmark in bookmarks_list[date]:
    #         urls_by_date.setdefault(date, set()).add(bookmark.text.url)
    #         bookmarks_by_url.setdefault(bookmark.text.url, []).append(bookmark)
    #
    # bookmark_counts_by_date = flask.g.user.bookmark_counts_by_date()

    return flask.render_template("bookmarks.html",
                                 bookmarks_by_url=data["bookmarks_by_url"],
                                 urls_by_date=data["urls_by_date"],
                                 sorted_dates=data["sorted_dates"],
                                 bookmark_counts_by_date=data["bookmark_counts_by_date"],
                                 )
        # ,
        #                          user=flask.g.user)


# These following endpoints are invoked via ajax calls from the bookmarks page

@account.route("/delete_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def delete(bookmark_id):
    return delete_bookmark(bookmark_id)


@account.route("/starred_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def starred_word(bookmark_id):
    return star_bookmark(bookmark_id)


@account.route("/unstarred_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def unstarred_word(bookmark_id):
    return unstar_bookmark(bookmark_id)
