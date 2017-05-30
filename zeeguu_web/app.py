# -*- coding: utf8 -*-
import os
import os.path
import flask
import flask_assets
import flask_sqlalchemy
from .cross_domain_app import CrossDomainApp
from zeeguu.util.configuration import load_configuration_or_abort




# *** Starting the App *** #
app = CrossDomainApp(__name__)


load_configuration_or_abort(app, 'ZEEGUU_WEB_CONFIG',
                            ['HOST', 'PORT', 'DEBUG', 'SECRET_KEY', 'MAX_SESSION',
                             'SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD',
                             'INVITATION_CODES'])


# The zeeguu.model  module relies on an app being injected from outside
# ----------------------------------------------------------------------
import zeeguu
zeeguu.app = app
import zeeguu.model
assert zeeguu.model
# -----------------

from .account import account
app.register_blueprint(account)

from .exercises import exercises
app.register_blueprint(exercises)

from umr import umrblue
app.register_blueprint(umrblue, url_prefix="/read")

env = flask_assets.Environment(app)
env.cache = app.instance_path
env.directory = os.path.join(app.instance_path, "gen")
env.url = "/gen"
env.append_path(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static"
), "/static")


# create the instance folder and return the path
def instance_path(app):
    path = os.path.join(app.instance_path, "gen")
    try:
        os.makedirs(path)
    except Exception as e:
        print(("exception" + str(e)))
        if not os.path.isdir(path):
            raise
    return path

instance = flask.Blueprint("instance", __name__, static_folder=instance_path(app))
app.register_blueprint(instance)


