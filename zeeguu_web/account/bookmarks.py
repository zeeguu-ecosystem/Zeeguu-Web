import datetime

from zeeguu_web.account.api.bookmarks import get_learned_bookmarks, get_bookmarks_by_date, star_bookmark, \
    report_learned_bookmark, \
    unstar_bookmark, delete_bookmark, \
    get_top_bookmarks, get_starred_bookmarks
from . import account, login_first
import flask


@account.route("/bookmarks")
@login_first
def bookmarks():
    # d = datetime.datetime.now() - datetime.timedelta(days=7)
    data = get_bookmarks_by_date()

    return flask.render_template("bookmarks.html",
                                 bookmarks_by_url=data["bookmarks_by_url"],
                                 urls_by_date=data["urls_by_date"],
                                 sorted_dates=data["sorted_dates"],
                                 bookmark_counts_by_date=data["bookmark_counts_by_date"],
                                 )


@account.route("/top_bookmarks")
@login_first
def top_bookmarks():
    bookmarks = get_top_bookmarks(10)

    return flask.render_template("bookmarks_top.html",
                                 bookmarks=bookmarks)


@account.route("/learned_bookmarks")
@login_first
def learned_bookmarks():
    bookmarks = get_learned_bookmarks()

    return flask.render_template("bookmarks_learned.html",
                                 bookmarks=bookmarks)


@account.route("/starred_bookmarks")
@login_first
def starred_bookmarks():
    bookmarks = get_starred_bookmarks()

    return flask.render_template("bookmarks_starred.html",
                                 bookmarks=bookmarks)


# These following endpoints are invoked via ajax calls from the bookmarks page
@account.route("/report_learned_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def post_report_learned_bookmark(bookmark_id):
    return report_learned_bookmark(bookmark_id)


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
