from . import account, login_first
import flask


@account.route("/reading")
@login_first
def reading():
    return flask.render_template("readingroom.html", user=flask.g.user)
