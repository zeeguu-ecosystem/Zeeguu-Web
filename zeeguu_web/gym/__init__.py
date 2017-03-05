# -*- coding: utf8 -*-
import flask
# We need to define the blueprint here, because all the files containing controllers use it
gym = flask.Blueprint("gym", __name__)
import views


