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
        cur = connection.cursor()
        try:
            cur.execute("select id, username, is_unb_account, max_storage_space, \
                (select id from Folder where Folder.user_id=User.id and Folder.parent_folder is NULL) as root_folder_id, \
                (select cast(ifnull(sum(size_bytes), 0) as SIGNED) from File where File.user_id=User.id) storage_used \
                from User, Session where Session.token=%s and User.id = Session.user_id", (session_token))
            connection.commit()

            result = cur.fetchone()
            if result is None:
                raise ZerodriveException(401, "Invalid session token.")
            
            cur.close()
            g.user_data = result
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred: {}".format(err.args[1]))
        finally:
            cur.close()
            
        return func(*args, **kwargs)
    return wrapper