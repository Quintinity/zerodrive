SESSION_TOKEN_LIFETIME = 1 # Number of days that session tokens live
SESSION_COOKIE_NAME = "session"

from flask import request, g, make_response, jsonify
from . import util
from .exceptions import ZerodriveException
from datetime import datetime
import pymysql

def requires_auth(func):
    def wrapper(*args, **kwargs):
        session_token = request.cookies.get(SESSION_COOKIE_NAME)
        if session_token is None:
            raise ZerodriveException(401, "You must be logged in to perform this action.")
        
        connection = util.open_db_connection()
        cur = connection.cursor()

        try:
            # Fetch all relevant user data 
            cur.execute("select id, username, is_unb_account, max_storage_space, expiry_time, \
                (select id from Folder where Folder.user_id=User.id and Folder.parent_folder is NULL) as root_folder_id, \
                (select cast(ifnull(sum(size_bytes), 0) as SIGNED) from File where File.user_id=User.id) as storage_used \
                from User, Session where Session.token=%s and User.id = Session.user_id", (session_token))
            connection.commit()
            
            result = cur.fetchone()

            if result is None:
                response = make_response((jsonify({"message": "Invalid session token"}), 400))
                response.set_cookie(SESSION_COOKIE_NAME, max_age=0)
                return response

            # Delete the session is it has expired and inform the user of this
            if result["expiry_time"] < datetime.utcnow():
                cur.execute("delete from Session where token = %s", (session_token))
                connection.commit()
                raise ZerodriveException(401, "This session has expired. Please login in again.")

            # This will refresh the token expiry time in the after_request event
            g.refresh_session_token = True

            del result["expiry_time"] # not needed as part of the user data
            g.session_token = session_token
            g.user_data = result
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred: {}".format(err.args[1]))
        finally:
            cur.close()
            
        return func(*args, **kwargs)
    return wrapper