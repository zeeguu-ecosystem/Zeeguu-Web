class APIConnectionError(Exception):
    def __init__(self, code):
        super()
        self.status_code = code

