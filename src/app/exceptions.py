##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from werkzeug.exceptions import HTTPException

class ZerodriveException(HTTPException):
    def __init__(self, code, message):
        Exception.__init__(self)
        self.code = code
        self.message = message
