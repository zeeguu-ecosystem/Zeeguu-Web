# -*- coding: utf8 -*-

"""

    Exports the exercises blueprint. 
    Currently all this does is embed the 
    already existing external exercises web app
    as an iframe    
     
"""

from functools import wraps

import flask

from zeeguu.model.user import User

# we define the blueprint here, and extended it in several files
exercises = flask.Blueprint("exercises", __name__)


@exercises.before_request
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

import endpoints
