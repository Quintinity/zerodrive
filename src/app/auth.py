SESSION_TOKEN_LIFETIME = 1 # Number of days that session tokens live
SESSION_COOKIE_NAME = "session"

from flask import request, g
from . import util
from .exceptions import ZerodriveException
import pymysql

def requires_auth(func):
    def wrapper(*args, **kwargs):
        session_token = request.cookies.get(SESSION_COOKIE_NAME)
        if session_token is None:
            raise ZerodriveException(401, "You must be logged in to perform this action.")
        
        connection = util.open_db_connection()

        try:
            cur = connection.cursor()
            cur.execute("select User.id, User.username from User, Session where Session.token=%s and User.id = Session.user_id", (session_token))
            connection.commit()

            result = cur.fetchone()
            if result is None:
                raise ZerodriveException(401, "Invalid session token.")
            
            cur.close()
            g.user_id = result["id"]
            g.username = result["username"]
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred: {}".format(err.args[1]))
        
        return func(*args, **kwargs)
    return wrapper