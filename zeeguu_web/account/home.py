import os

from flask import send_from_directory

from . import account
import flask
import zeeguu


@account.route("/")
def home():
    if "user" in flask.session:
        return flask.redirect(flask.url_for("account.bookmarks"))
    return flask.render_template("index.html")


@account.route("/favicon.ico")
def get_favicon():
    return send_from_directory(os.path.join(zeeguu.app.root_path, 'static'), 'img/favicon.ico')


