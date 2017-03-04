# -*- coding: utf8 -*-
import os
import os.path
import flask
import flask_assets
import flask_sqlalchemy


class CrossDomainApp(flask.Flask):
    """Allows cross-domain requests for all error pages"""
    def handle_user_exception(self, e):
        rv = super(CrossDomainApp, self).handle_user_exception(e)
        rv = self.make_response(rv)
        rv.headers['Access-Control-Allow-Origin'] = "*"
        return rv


# create the instance folder and return the path
def instance_path(app):
    path = os.path.join(app.instance_path, "gen")
    try:
        os.makedirs(path)
    except Exception as e:
        print ("exception" + str(e))
        if not os.path.isdir(path):
            raise
    return path

# *** Starting the App *** #
app = CrossDomainApp(__name__, instance_relative_config=True)

instance = flask.Blueprint("instance", __name__, static_folder=instance_path(app))

app.config.from_object("zeeguu_web.default_config") # this means the default_config file from the zeeguu_web module
app.config.from_pyfile("config.cfg", silent=True) #config.cfg is in the instance folder;
# since for the tests the config.cfg is not found, they run only with the default_config; silent = True is useful
# so the program does not stop if the config file is not found


# the zeeguu core model expects a bunch of configuration stuff to be available in the zeeguu.app.config
# we bind our current app.config to the zeeguu.app.config so that code does not break.
import zeeguu
zeeguu.app = app
zeeguu.app.config = app.config

# Important... let's initialize the models with a db object
db = flask_sqlalchemy.SQLAlchemy()
zeeguu.db = db
import zeeguu.model
# -------------------------------

env = flask_assets.Environment(app)
env.cache = app.instance_path
env.directory = os.path.join(app.instance_path, "gen")
env.url = "/gen"
env.append_path(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static"
), "/static")

db.init_app(app)
db.create_all(app=app)


from gym import gym
from account import account

app.register_blueprint(instance)
app.register_blueprint(gym)
app.register_blueprint(account)