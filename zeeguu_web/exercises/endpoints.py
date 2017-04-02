from . import exercises, login_first
import flask


@exercises.route("/exercises")
@login_first
def exercises():
    return flask.render_template("exercises.html", user=flask.g.user)
