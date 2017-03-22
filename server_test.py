#!/bin/env python
from zeeguu_web.app import app as application
import zeeguu
application.logger.debug (application.instance_path)
application.logger.debug ("Running with DB " + zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI"))


application.run(
     host=application.config.get("HOST", "localhost"),
     port=application.config.get("PORT", 9000)
)
