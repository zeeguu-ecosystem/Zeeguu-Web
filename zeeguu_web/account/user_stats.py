from zeeguu_web.account.api.user_stats import bookmark_counts_by_date
from . import account, login_first
import flask


@account.route("/stats", methods=["GET"])
@login_first
def stats():
    return flask.render_template("user_stats.html",
                                 bookmark_counts_by_date=bookmark_counts_by_date())
