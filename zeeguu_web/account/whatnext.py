from flask import redirect, make_response

from zeeguu_web.api_communication import is_teacher, upload_user_activity_data

from . import account
from zeeguu_web.crosscutting_concerns import login_first

import flask


@account.route("/whatnext")
@login_first
def whatnext():
    return flask.render_template("account/whatnext.html", is_teacher=is_teacher())


@account.route("/aiki")
@login_first
def aiki():
    upload_user_activity_data({'tralala':'lala'})

    if flask.request.environ.get('HTTP_ORIGIN', None) is not None:
        print(flask.request.environ['HTTP_ORIGIN'])


    return make_response(redirect(flask.url_for("reader_blueprint.articles")))
