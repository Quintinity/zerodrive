SESSION_TOKEN_LIFETIME = 1 # Number of days that session tokens live
SESSION_COOKIE_NAME = "session"

from flask import request, g
from . import util
import pymysql

def requires_auth(func):
    def wrapper(*args, **kwargs):
        session_token = request.cookies.get(SESSION_COOKIE_NAME)
        if session_token is None:
            return {"error": "You must be logged in to perform this action."}, 401
        
        connection = util.open_db_connection()
        if connection is None:
            return {"error": "Failed to connect to database."}, 500

        try:
            cur = connection.cursor()
            cur.execute("select User.id, User.email from User, Session where Session.token=%s and User.id = Session.user_id", (session_token))
            connection.commit()

            result = cur.fetchone()
            print(result)
            if result is None:
                return {"error": "Invalid session token."}, 401
            
            cur.close()
            g.user_id = result["id"]
            g.email = result["email"]
        except pymysql.MySQLError as err:
            return {"error": "A database error has occurred: {}".format(err.args[1])}, 500
        
        return func(*args, **kwargs)
    return wrapper