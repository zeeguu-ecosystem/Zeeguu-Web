# -*- coding: utf8 -*-
from functools import wraps

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


def login_first(fun):
    """
    Function Wrapper 
    
    Makes sure that the user is logged_in.
    If not, appends the intended url to the login url,
    and redirects to login.
    """
    @wraps(fun)
    def decorated_function(*args, **kwargs):
        if "user" in flask.session:
            flask.g.user = User.query.get(flask.session["user"])
        else:
            flask.g.user = None

        if flask.g.user:
            return fun(*args, **kwargs)
        else:
            next_url = flask.request.url
            login_url = '%s?next=%s' % (flask.url_for('account.login'), next_url)
            return flask.redirect(login_url)
    return decorated_function


import bookmarks
import creation
import home
import login
import reading
import reset_pass
import static_pages
import user_stats


