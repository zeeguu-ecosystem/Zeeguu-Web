from . import account, login_first
import flask

from zeeguu.model import SimpleKnowledgeEstimator, Session
import zeeguu


@account.route("/watch_connect", methods=["GET"])
@login_first
def watch_connect():

    s = Session.find_for_user(flask.g.user)
    zeeguu.db.session.add(s)
    zeeguu.db.session.commit()

    session_id = str(s.id).zfill(8)
    watch_connect = session_id[:4] + "-" + session_id[4:]

    return flask.render_template("watch_connect.html",
                                 user=flask.g.user,
                                 smartwatch_login_code=watch_connect)
