from . import account
import flask


@account.route("/")
def home():
    if "user" in flask.session:
        return flask.redirect(flask.url_for("account.bookmarks"))
    return flask.render_template("index.html")
