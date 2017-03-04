from functools import wraps
import flask
from . import gym
from zeeguu.model import User


@gym.before_request
def setup():
    # Code moved to login_first
    pass

def login_first(fun):
    """
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
            login_url = '%s?next=%s' % (flask.url_for('gym.login'), next_url)
            return flask.redirect(login_url)
    return decorated_function
