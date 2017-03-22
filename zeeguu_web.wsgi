#!/bin/env python
import zeeguu
from zeeguu_web.app import app as application

application.logger.debug (application.instance_path)
application.logger.debug ("Running with DB " + zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI"))
