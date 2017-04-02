from . import account, login_first
import flask

from zeeguu.model import SimpleKnowledgeEstimator, Session
import zeeguu


@account.route("/my_account", methods=["GET"])
@login_first
def my_account():

    estimator = SimpleKnowledgeEstimator(flask.g.user, flask.g.user.learned_language_id)

    # get learner_stats_data for the line_graph
    learner_stats_data = flask.g.user.learner_stats_data()

    s = Session.find_for_user(flask.g.user)
    zeeguu.db.session.add(s)
    zeeguu.db.session.commit()

    session_id = str(s.id).zfill(8)
    smartwatch_login_code = session_id[:4] + "-" + session_id[4:]

    return flask.render_template("my_account.html",
                                 user=flask.g.user,
                                 estimator=estimator,
                                 learner_stats_data=learner_stats_data,
                                 smartwatch_login_code=smartwatch_login_code)
