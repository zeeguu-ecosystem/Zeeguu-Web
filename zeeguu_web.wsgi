#!/bin/env python
from zeeguu_web.app import app as application
application.logger.debug (application.instance_path)
application.logger.debug (application.config.get("SQLALCHEMY_DATABASE_URI"))