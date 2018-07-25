# -*- coding: utf8 -*-
from functools import wraps

import flask

from zeeguu_web.account.api.session_management import validate
from zeeguu_web.constants import KEY__SESSION_ID, KEY__USER_NAME

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

        if KEY__SESSION_ID in flask.session:
            try:
                result = validate()
                if result:
                    flask.g.username = flask.session[KEY__USER_NAME]
                    return fun(*args, **kwargs)
            except Exception as e:
                print(e)

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
