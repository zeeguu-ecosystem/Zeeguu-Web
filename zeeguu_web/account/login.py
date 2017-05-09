import zeeguu
from flask import make_response, redirect

from . import account, login_first
import flask
from zeeguu.model import User, Session


@account.route("/login", methods=("GET", "POST"))
def login():
    """
    
        check user credentials 
        
        if it contains the ?next=... parameter, it will redirect
        to there on success 
        
    :return: 
    """
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

                session = Session.for_user(user)
                zeeguu.db.session.add(session)
                zeeguu.db.session.commit()

                response = make_response(redirect(flask.request.args.get("next") or flask.url_for("account.bookmarks")))
                response.set_cookie('sessionID', str(session.id), max_age=31536000)
                return response

    return flask.render_template("login.html")


@account.route("/login_with_session", methods=["POST"])
def login_with_session():
    """
    Call this with a post parameter session_id
    The server will remember that the user is logged in,
    so you can display pages w/o being redirected to the
    login screen.

    Mainly designed with the mobile apps in mind, apps which
    might want to display exercises in a webview. 
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


@account.route("/logout")
@login_first
def logout():
    # Note, that there is also an API endpoint for logout called logout_session
    flask.session.pop("user", None)
    return flask.redirect(flask.url_for("account.home"))


@account.route("/logged_in")
@login_first
def logged_in():
    if flask.session.get("user", None):
        return "YES"
    return "NO"
