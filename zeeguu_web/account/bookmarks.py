from . import account, login_first
import flask
from zeeguu.model import UserWord, User, Bookmark, Text
import zeeguu


@account.route("/bookmarks")
@login_first
def bookmarks():
    bookmarks_list,dates = flask.g.user.bookmarks_by_date()

    most_recent_seven_days = dates[0:6]

    urls_by_date = {}
    bookmarks_by_url = {}
    for date in most_recent_seven_days:
        for bookmark in bookmarks_list[date]:
            urls_by_date.setdefault(date, set()).add(bookmark.text.url)
            bookmarks_by_url.setdefault(bookmark.text.url,[]).append(bookmark)

    bookmark_counts_by_date = flask.g.user.bookmark_counts_by_date()

    if most_recent_seven_days:
        return flask.render_template("bookmarks.html",
                                     bookmarks_by_url=bookmarks_by_url,
                                     urls_by_date=urls_by_date,
                                     sorted_dates=most_recent_seven_days,
                                     bookmark_counts_by_date=bookmark_counts_by_date,
                                     user=flask.g.user)

    return flask.render_template("welcome_bookmarks.html", username=flask.g.user.name, bookmark_counts_by_date=bookmark_counts_by_date)

# These following endpoints are invoked via ajax calls from the bookmarks page

@account.route("/delete_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def delete(bookmark_id):

    # Beware, the there is another delete_bookmark in the zeeguu API!!!
    bookmark = Bookmark.query.get(bookmark_id)
    if not bookmark:
        return "Not found"

    text = Text.query.get(bookmark.text.id)

    # bookmark goes
    zeeguu.db.session.delete(bookmark)

    # If no more bookmarks point to the text, text goes too
    if not (text.all_bookmarks()):
        zeeguu.db.session.delete(text)

    zeeguu.db.session.commit()

    return "OK"


@account.route("/starred_word/<word_id>/<user_id>", methods=("POST",))
@login_first
def starred_word(word_id,user_id):
    word = UserWord.query.get(word_id)
    user = User.find_by_id(user_id)
    user.star(word)
    zeeguu.db.session.commit()
    return "OK"


@account.route("/unstarred_word/<word_id>/<user_id>", methods=("POST",))
@login_first
def unstarred_word(word_id,user_id):
    word = UserWord.query.get(word_id)
    user = User.find_by_id(user_id)
    user.starred_words.remove(word)
    zeeguu.db.session.commit()
    print(str(word) + " is now *unstarred* for user " + user.name)
    return "OK"
