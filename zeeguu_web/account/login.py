import flask
from flask import make_response, redirect
from flask import flash

from zeeguu_web.account.api import session_management, account_management
from zeeguu_web.account.api.api_connection import APIException
from zeeguu_web.account.api.languages import get_available_languages, get_available_native_languages
from zeeguu_web.account.api.session_management import user_details
from zeeguu_web.app import configuration
from zeeguu_web.constants import *

from . import account, login_first


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

    return flask.render_template("login.html")


@account.route("/create_account", methods=("GET", "POST"))
def create_account():
    # A cool way of passing the arguments to the flask template
    template_arguments = dict(
        languages=get_available_languages(),
        native_languages=get_available_native_languages(),
        default_learned=DEFAULT_LANGUAGE
    )

    # GET
    if flask.request.method == "GET":
        return flask.render_template("create_account.html", **template_arguments)

    # POST
    form = flask.request.form
    password = form.get("password", None)
    email = form.get("email", None)
    name = form.get("name", None)
    code = form.get("code", None)
    language = form.get("language", None)
    native_language = form.get("native_language", None)

    if password is None or email is None or name is None:
        flash("Please enter your name, email address, and password")

    else:
        try:

            sessionID = account_management.create_account(email, name, password, language,
                                                          native_language, invite_code=code)  # setting registration code is not possible

            response = make_response(flask.redirect(flask.url_for("account.whatnext")))

            details = user_details(sessionID)

            _set_session_data(details, sessionID, response)

            return response

        except ValueError:
            flash("Username could not be created. Please contact us.")
        except APIException as e:
            flask.flash(e.message)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            flash("Something went wrong. Please contact us.")

    return flask.render_template("create_account.html", **template_arguments)


@account.route("/logout")
@login_first
def logout():
    try:
        session_management.logout()
    except APIException:
        print("Logout at server failed, still removing session key.")

    for key in SESSION_KEYS:
        flask.session.pop(key, None)

    response = make_response(redirect(flask.url_for("account.home")))
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
