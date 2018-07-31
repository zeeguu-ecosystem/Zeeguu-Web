from flask import url_for

from zeeguu_web.account.api.teacher import is_teacher
from zeeguu_web.constants import KEY__SESSION_ID

from . import account, login_first
import flask


@account.route("/favicon.ico")
def get_favicon():
    return flask.redirect(url_for('static', filename='img/favicon.ico'))


@account.route("/")
def home():
    if KEY__SESSION_ID in flask.session:
        return flask.redirect(flask.url_for("account.whatnext"))
    return flask.render_template("index.html")


@account.route("/whatnext")
@login_first
def whatnext():
    return flask.render_template("whatnext.html", is_teacher=is_teacher())
