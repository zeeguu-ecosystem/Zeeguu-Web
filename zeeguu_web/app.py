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


def assert_configs(config, required_keys):
    for key in required_keys:
        config_value = config.get(key)
        assert config_value, "Please define the {key} key in the config file!".format(key=key)


def select_config_file():
    # Default config
    # app.config.from_object("default_config")

    # Loading the default user configuration
    config_file = os.path.expanduser('~/.config/zeeguu/web.cfg')

    # The default config files could be overwritten by the os.environ variable
    if os.environ.has_key("CONFIG_FILE"):
        config_file = os.environ["CONFIG_FILE"]

    print ('running with config file: ' + config_file)

    return config_file

# *** Starting the App *** #
app = CrossDomainApp(__name__, instance_relative_config=False)

app.config.from_pyfile(os.path.expanduser(select_config_file()), silent=False)

instance = flask.Blueprint("instance", __name__, static_folder=instance_path(app))

print ('DB is: ' + app.config["SQLALCHEMY_DATABASE_URI"])

# here we used to use the instance folder [1], but eventually decided to go for the ./zeeguu/folder:
# http://flask.pocoo.org/docs/0.11/config/#instance-folders

# the zeeguu core model expects a bunch of configuration stuff to be available in the zeeguu.app.config
# we bind our current app.config to the zeeguu.app.config so that code does not break.
import zeeguu
zeeguu.app = app
zeeguu.app.config = app.config

assert_configs(app.config, ['HOST', 'PORT', 'DEBUG', 'SECRET_KEY', 'MAX_SESSION',
                            'SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD'])

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
