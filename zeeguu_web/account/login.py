import flask
from flask import make_response, redirect

from zeeguu_web.account.api import session_management
from zeeguu_web.account.api.api_connection import APIException
from zeeguu_web.account.api.session_management import user_details
from zeeguu_web.constants import *

from . import account

from zeeguu_web.crosscutting_concerns import login_first


@account.route("/login", methods=("GET", "POST"))
def login():
    """
    
        check user credentials 
        
        if next=... parameter is present redirect on success
        
    """

    form = flask.request.form
    if flask.request.method == "POST" and form.get("login", False):
        password = form.get("password", None)
        email = form.get("email", None)

        if password is None or email is None:
            flask.flash("Please enter your email address and password")
        else:
            try:
                sessionID = session_management.login(email, password)
                details = user_details(sessionID)
            except APIException as e:
                flask.flash(e.message)

            else:
                response = make_response(redirect(flask.request.args.get("next") or flask.url_for("account.whatnext")))

                _set_session_data(details, sessionID, response)

                return response

    return flask.render_template("account/login.html")


@account.route("/logout")
@login_first
def logout():
    try:
        session_management.logout()
    except APIException:
        print("Logout at server failed, still removing session key.")

    for key in SESSION_KEYS:
        flask.session.pop(key, None)

    response = make_response(redirect(flask.url_for("static_pages.index")))
    response.delete_cookie(KEY__STAND_ALONE_SESSION_ID)
    response.delete_cookie(KEY__FLASK_SESSION)
    response.delete_cookie(KEY__NATIVE_LANG)
    return response


@account.route("/logged_in")
@login_first
def logged_in():
    if flask.session.get(KEY__SESSION_ID, None):
        return "YES"
    return "NO"


def _set_session_data(details, sessionID, response):
    """
    Set session information for later usage
    """

    flask.session[KEY__SESSION_ID] = sessionID
    flask.session[KEY__USER_NAME] = details["name"]

    flask.session.permanent = True

    response.set_cookie(KEY__STAND_ALONE_SESSION_ID, str(sessionID), max_age=31536000)
    response.set_cookie(KEY__NATIVE_LANG, details["native_language"], max_age=31536000)
