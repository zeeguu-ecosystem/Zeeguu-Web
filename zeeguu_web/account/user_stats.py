from . import account, login_first
import flask

from zeeguu.model import SimpleKnowledgeEstimator, Session


@account.route("/stats", methods=["GET"])
@login_first
def stats():
    estimator = SimpleKnowledgeEstimator(flask.g.user, flask.g.user.learned_language_id)
    learner_stats_data = flask.g.user.learner_stats_data()

    bookmark_counts_by_date = flask.g.user.bookmark_counts_by_date()

    return flask.render_template("user_stats.html",
                                 user=flask.g.user,
                                 estimator=estimator,
                                 learner_stats_data=learner_stats_data,
                                 bookmark_counts_by_date=bookmark_counts_by_date)
