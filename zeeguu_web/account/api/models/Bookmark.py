class Bookmark:

    def __init__(self, id, to, from_lang, to_lang, title, url, origin_importance, from_):
        self.id = id
        self.to = to
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.title = title
        self.url = url
        self.origin_importance = origin_importance
        self.from_ = from_

    @classmethod
    def from_json(cls, _json):
        id = _json["id"]
        to = _json["to"]
        from_lang = _json["from_lang"]
        to_lang = _json["to_lang"]
        title = _json["title"]
        url = _json["url"]
        origin_importance = _json["origin_importance"]
        from_ = _json["from"]

        return Bookmark(id, to, from_lang, to_lang, title, url, origin_importance, from_)