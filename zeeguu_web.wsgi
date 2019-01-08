#!/bin/env python
import zeeguu_core
from zeeguu_web.app import app as application

application.logger.debug (application.instance_path)
