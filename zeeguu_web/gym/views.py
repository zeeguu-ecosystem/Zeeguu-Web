import flask
from flask import redirect

from views_utils import login_first
from . import gym
from zeeguu.model.session import Session
from zeeguu.model.user import User
from zeeguu.model.user_word import UserWord
import zeeguu


@gym.route("/")
def home():
    if "user" in flask.session:
        return flask.redirect(flask.url_for("gym.bookmarks"))
    return flask.render_template("index.html")


@gym.route("/login", methods=("GET", "POST"))
def login():
    form = flask.request.form
    if flask.request.method == "POST" and form.get("login", False):
        password = form.get("password", None)
        email = form.get("email", None)
        if password is None or email is None:
            flask.flash("Please enter your email address and password")
        else:
            user = User.authorize(email, password)
            if user is None:
                flask.flash("Invalid email and password combination")
            else:
                flask.session["user"] = user.id
                flask.session.permanent = True
                return flask.redirect(flask.request.args.get("next") or flask.url_for("gym.bookmarks"))
    return flask.render_template("login.html")


@gym.route("/login_with_session", methods=["POST"])
def login_with_session():
    """
    Call this with a post parameter session_id
    The server will remember that the user is logged in,
    so you can display pages w/o being redirected to the
    login screen.

    Mainly designed with the mobile apps in mind, apps which
    might want to display exercises in a webview. For that, check
    out /m_recognize
    :return:
    """
    form = flask.request.form
    session_string = form.get("session_id", 0)
    session = Session.find_for_id(session_string)

    if session:
        user = session.user
        flask.g.user = user
        flask.session["user"] = user.id
    else:
        print "somebody tried to login_with_session but failed. " \
              "however we are still keeping the current session if it exists"
        return "FAIL"

    return "OK"


@gym.route("/logout")
@login_first
def logout():
    # Note, that there is also an API endpoint for logout called logout_session
    flask.session.pop("user", None)
    return flask.redirect(flask.url_for("gym.home"))


@gym.route("/logged_in")
def logged_in():
    if flask.session.get("user", None):
        return "YES"
    return "NO"


@gym.route("/bookmarks")
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

    print ("before rendering the template!!!!! ")
    return flask.render_template("bookmarks.html",
                                 bookmarks_by_url=bookmarks_by_url,
                                 urls_by_date=urls_by_date,
                                 sorted_dates=most_recent_seven_days,
                                 bookmark_counts_by_date=bookmark_counts_by_date,
                                 user=flask.g.user)


@gym.route("/reading")
@login_first
def reading():
    return flask.render_template("readingroom.html", user=flask.g.user)


@gym.route("/exercises")
@login_first
def exercises():
    return flask.render_template("exercises.html", user=flask.g.user)


@gym.route("/prinz")
def prinz():
    return flask.render_template("prinz.html")


@gym.route("/install")
def install():
    return flask.render_template("install.html")


@gym.route("/chrome")
def chrome():
    return redirect("https://chrome.google.com/webstore/detail/zeeguu/ckncjmaednfephhbpeookmknhmjjodcd?hl=en", code=302)


@gym.route("/gym/starred_word/<word_id>/<user_id>", methods=("POST",))
@login_first
def starred_word(word_id,user_id):
    word = UserWord.query.get(word_id)
    user = User.find_by_id(user_id)
    user.star(word)
    zeeguu.db.session.commit()
    return "OK"


@gym.route("/gym/unstarred_word/<word_id>/<user_id>", methods=("POST",))
@login_first
def unstarred_word(word_id,user_id):
    word = UserWord.query.get(word_id)
    user = User.find_by_id(user_id)
    user.starred_words.remove(word)
    zeeguu.db.session.commit()
    print word + " is now *unstarred* for user " + user.name
    return "OK"


