from zeeguu_web.account.api.teacher import is_teacher

from . import account
from zeeguu_web.crosscutting_concerns import login_first

import flask


@account.route("/whatnext")
@login_first
def whatnext():
    return flask.render_template("account/whatnext.html", is_teacher=is_teacher())
