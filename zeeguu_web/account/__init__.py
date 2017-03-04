# -*- coding: utf8 -*-

import flask

from zeeguu.model.user import User

# we define the blueprint here, and extended it in several files
account = flask.Blueprint("account", __name__)

@account.before_request
def setup():
    if "user" in flask.session:
        flask.g.user = User.query.get(flask.session["user"])
    else:
        flask.g.user = None

import create_and_show
import reset_pass

