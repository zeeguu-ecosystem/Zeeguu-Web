#!/usr/bin/env python
# -*- coding: utf8 -*-

import app
application = app.app

# from zeeguu.model.ranked_word import RankedWord
# with app.app_context():
#     RankedWord.cache_ranked_words()

print "Instance folder:", application.instance_path
application.run(
    host=application.config.get("HOST", "localhost"),
    port=application.config.get("PORT", 9002)
)            
