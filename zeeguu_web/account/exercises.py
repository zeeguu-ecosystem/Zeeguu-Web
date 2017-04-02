from . import account, login_first
import flask


@account.route("/exercises")
@login_first
def exercises():
    return flask.render_template("exercises.html", user=flask.g.user)
