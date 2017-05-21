from . import account, login_first
import flask


@account.route("/reading")
@login_first
def reading():
    # inform everybody that this is deprecated
    return flask.redirect(flask.url_for("umrblue.articles"))
