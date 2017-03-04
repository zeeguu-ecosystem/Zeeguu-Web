import flask_sqlalchemy
import zeeguu
zeeguu.db = flask_sqlalchemy.SQLAlchemy()

from zeeguu_web import app
import zeeguu_web

zeeguu.db.init_app(app)
zeeguu.db.create_all(app=app)

from zeeguu.model.user import User

with zeeguu_web.app.app_context():
	mir = User.find("i@mir.lu")
	print mir