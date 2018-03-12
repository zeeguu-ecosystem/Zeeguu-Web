import requests
import zeeguu
from flask import make_response, redirect

from zeeguu_web.account.api import session_management, account_management
from zeeguu_web.account.api.api_exceptions import APIConnectionError
from . import account, login_first
import flask
from zeeguu.model import User, Session

from flask import flash
from zeeguu.model.language import Language
import sqlalchemy.exc

KEY_USER_ID = "user_id"
KEY_USER_NAME = "user_name"
SESSION_ID = "session_id"

SESSION_KEYS = [KEY_USER_ID, KEY_USER_NAME, SESSION_ID]


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
            except APIConnectionError as e:
                if e.status_code is 400 or e.status_code is 401:
                    flask.flash("Invalid email and password combination")
                    return
                else:
                    flask.flash("Connection error, please try again later.")

            else:
                test1 = flask.request.args.get("next")
                test2 =flask.url_for("account.whatnext")
                response = make_response(redirect(test1 or test2))

                _set_session_id(sessionID, response)

                return response


    return flask.render_template("login.html")


@account.route("/create_account", methods=("GET", "POST"))
def create_account():

    # A cool way of passing the arguments to the flask template
    template_arguments = dict (
         languages= Language.available_languages(),
         native_languages = Language.native_languages(),
         default_learned= Language.default_learned()
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
    language = Language.find(form.get("language", None))
    native_language = Language.find(form.get("native_language", None))

    if not code in zeeguu.app.config.get("INVITATION_CODES"):
        flash("Invitation code is not recognized. Please contact us.")

    if password is None or email is None or name is None:
        flash("Please enter your name, email address, and password")

    else:
        try:

            session = account_management.create_account(email, name, password, language, native_language) #setting registration code is not possible

            response = make_response(flask.redirect(flask.url_for("account.whatnext")))
            _set_session_id(session, response)

            return response

        except ValueError:
            flash("Username could not be created. Please contact us.")
        except APIConnectionError as e:
            if e.status_code is 400 or e.status_code is 401:
                flask.flash("Invalid email and password combination")
                return
            else:
                flask.flash("Connection error, please try again later.")
        except:
            flash("Something went wrong. Please contact us.")
        finally:
            zeeguu.db.session.rollback()

    return flask.render_template("create_account.html", **template_arguments)


@account.route("/logout")
@login_first
def logout():
    try:
        session_management.logout()
    except APIConnectionError:
        print("Logout at server failed, still removing session key.")

    for key in SESSION_KEYS:
        flask.session.pop(key, None)

    return make_response(redirect(flask.url_for("account.home")))


@account.route("/logged_in")
@login_first
def logged_in():
    if flask.session.get("session_id", None):
        return "YES"
    return "NO"


def _set_session_data(user: User, response):
    """
        extracted to its own function, since it's duplicated between login and create_account
    """

    api_session = Session.find_for_user(user)
    zeeguu.db.session.add(api_session)
    zeeguu.db.session.commit()

    flask.session[KEY_USER_ID] = user.id
    flask.session[KEY_USER_NAME] = user.name
    flask.session[SESSION_ID] = api_session.id

    flask.session.permanent = True

    response.set_cookie('sessionID', str(api_session.id), max_age=31536000)

def _set_session_id(sessionID, response):
    """
    Set session information for later usage
    """
    flask.session[SESSION_ID] = sessionID

    flask.session.permanent = True

    response.set_cookie('sessionID', str(sessionID), max_age=31536000)


# @account.route("/login_with_session", methods=["POST"])
# def login_with_session():
#     """
#     Call this with a post parameter session_id
#     The server will remember that the user is logged in,
#     so you can display pages w/o being redirected to the
#     login screen.
#
#     Mainly designed with the mobile apps in mind, apps which
#     might want to display exercises in a webview.
#     :return:
#     """
#     form = flask.request.form
#     session_string = form.get("session_id", 0)
#     session = Session.find_for_id(session_string)
#
#     if session:
#         user = session.user
#         flask.g.user = user
#         flask.session["user_id"] = user.id
#     else:
#         print("somebody tried to login_with_session but failed. " \
#               "however we are still keeping the current session if it exists")
#         return "FAIL"
#
#     return "OK"
