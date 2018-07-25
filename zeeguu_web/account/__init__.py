# -*- coding: utf8 -*-
from functools import wraps

import flask

from zeeguu_web.constants import KEY__SESSION_ID

# we define the blueprint here, and extended it in several files
account = flask.Blueprint("account", __name__)


def login_first(fun):
    """

    Function Wrapper

    Makes sure that the user is logged_in.

    If not, appends the intended url to the login url and redirects to login.

    """

    @wraps(fun)
    def decorated_function(*args, **kwargs):
        from zeeguu.model import Session

        flask.g.user = None
        if KEY__SESSION_ID in flask.session:
            session = Session.query.get(flask.session[KEY__SESSION_ID])
            if session is not None:
                flask.g.user = session.user
                return fun(*args, **kwargs)

        next_url = flask.request.url
        login_url = '%s?next=%s' % (flask.url_for('account.login'), next_url)
        return flask.redirect(login_url)

    return decorated_function


from . import bookmarks
from . import home
from . import login
from . import reset_pass
from . import static_pages
from . import user_stats
from . import watch_connect
