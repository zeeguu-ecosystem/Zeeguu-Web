# -*- coding: utf8 -*-
from functools import wraps

import flask
from zeeguu.model import Session

from zeeguu.model.user import User

# we define the blueprint here, and extended it in several files
account = flask.Blueprint("account", __name__)


@account.before_request
def setup():
    if "user_id" in flask.session:
        flask.g.user = User.query.get(flask.session["user_id"])
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
        if "session_id" in flask.session:
            session = Session.query.get(flask.session["session_id"])
            if session is None:
                flask.g.user = None
            else:
                flask.g.user = session.user
        else:
            flask.g.user = None

        if "session_id" in flask.session:
            return fun(*args, **kwargs)
        else:
            next_url = flask.request.url
            login_url = '%s?next=%s' % (flask.url_for('account.login'), next_url)
            return flask.redirect(login_url)
    return decorated_function


from . import bookmarks
from . import home
from . import login
from . import reading
from . import reset_pass
from . import static_pages
from . import user_stats
from . import teacher
from . import watch_connect


