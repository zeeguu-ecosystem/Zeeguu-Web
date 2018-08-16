import urllib


class URL():
    def __init__(self, url, title):
        self.url = url
        self.title = title

    def escaped(self):
        return urllib.parse.quote_plus(self.url)
