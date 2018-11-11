from werkzeug.exceptions import HTTPException

class ZerodriveException(HTTPException):
    def __init__(self, code, message):
        Exception.__init__(self)
        self.code = code
        self.message = message
