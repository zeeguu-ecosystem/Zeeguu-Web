#!/bin/env python
import zeeguu_web
zeeguu_web.app.logger.debug (zeeguu_web.app.instance_path)
zeeguu_web.app.logger.debug (zeeguu_web.app.config.get("SQLALCHEMY_DATABASE_URI"))
from zeeguu_web import app as application
