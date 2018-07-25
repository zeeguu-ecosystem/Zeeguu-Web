import os

from flask import send_from_directory

from zeeguu_web.account.api.teacher import is_teacher
from zeeguu_web.constants import KEY__SESSION_ID

from . import account, login_first
import flask
import zeeguu


# cf. http://flask.pocoo.org/docs/0.12/patterns/favicon/
@account.route("/favicon.ico")
def get_favicon():
    return send_from_directory(os.path.join(zeeguu.app.root_path, 'static'), 'img/favicon.ico')


@account.route("/")
def home():
    print(flask.session)
    if KEY__SESSION_ID in flask.session:
        return flask.redirect(flask.url_for("account.whatnext"))
    return flask.render_template("index.html")


@account.route("/whatnext")
@login_first
def whatnext():
    return flask.render_template("whatnext.html", user=flask.g.user, is_teacher=is_teacher())
