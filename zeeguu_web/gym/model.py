# -*- coding: utf8 -*-
import datetime

from zeeguu import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))
    bookmark = db.relationship("Bookmark", backref="card")
    last_seen = db.Column(db.DateTime)

    def __init__(self, bookmark):
        self.bookmark = bookmark
        self.position = 0
        self.reason = ""
        self.seen()

    def seen(self):
        self.last_seen = datetime.datetime.now()

    def set_reason(self, reason):
        self.reason = reason

    def reason(self):
        return self.reason

    def is_starred(self):
        return self.bookmark.user.has_starred(self.bookmark.origin)

    def star(self):
        word = self.bookmark.origin
        self.bookmark.user.starred_words.append(word)

    def unstar(self):
        word = self.bookmark.origin
        self.bookmark.user.starred_words.remove(word)
