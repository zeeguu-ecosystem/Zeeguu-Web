import os

from flask import send_from_directory
from zeeguu.model.teacher import Teacher

from . import account, login_first
import flask
import zeeguu


# cf. http://flask.pocoo.org/docs/0.12/patterns/favicon/
@account.route("/favicon.ico")
def get_favicon():
    return send_from_directory(os.path.join(zeeguu.app.root_path, 'static'), 'img/favicon.ico')


@account.route("/")
def home():
    print (flask.session)
    if "session_id" in flask.session:
        return flask.redirect(flask.url_for("account.whatnext"))
    return flask.render_template("index.html")


@account.route("/whatnext")
@login_first
def whatnext():
    is_teacher = Teacher.from_user(flask.g.user) is not None
    return flask.render_template("whatnext.html", user=flask.g.user, is_teacher=is_teacher)
