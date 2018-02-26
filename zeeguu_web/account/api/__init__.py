class APIConnectionError(Exception):
    def __init__(self, code):
        super()
        self.status_code = code

def retrievePayload(response):
    if response.status_code is 200:
        return response
    else :
        raise APIConnectionError(response.status_code)

