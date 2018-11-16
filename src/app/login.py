##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask_restful import Resource
from flask import request, make_response
from hashlib import sha256
from datetime import datetime
from . import util, auth, config, ZerodriveException
from .user import MAX_STORAGE_SPACE
import pymysql, ldap3, os

class Login(Resource):
    def __init__(self):
        self.ldap_server_unb = ldap3.Server(host=config.ldap_unb["host"], port=config.ldap_unb["port"])
        self.ldap_server_dev = ldap3.Server(host=config.ldap_dev["host"], port=config.ldap_dev["port"])

    # Authenticate against the database, for local accounts.
    # Returns the user ID if successful, None otherwise.
    def auth_db(self, username, password):
        db_connection = util.open_db_connection()
        cur = db_connection.cursor()
        cur.execute("select id, hashpw, salt from User where username = %s", (username))
        db_connection.commit()

        # Validate credentials
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        given_hashpw = sha256((password + result["salt"]).encode("UTF-8")).digest().hex()

        return result["id"] if given_hashpw == result["hashpw"] else None
    
    # Authenticate against an LDAP.
    # Returns the user ID if successful, None otherwise.
    # If authentication succeeds but 
    def auth_ldap(self, username, password, ldap_server, use_tls):
        try:
            ldap_connection = ldap3.Connection(ldap_server, user="uid={},ou=People,ou=fcs,o=unb".format(username), password=password)
            ldap_connection.open()
            if use_tls:
                ldap_connection.start_tls()
            ldap_connection.bind()
            ldap_connection.unbind()

            if ldap_connection.result["result"] == 49: # Invalid credentials
                return None
            elif ldap_connection.result["result"] != 0:
                raise ZerodriveException(500, "An unknown LDAP error has occurred: {}.".format(ldap_connection.result["result"]))

            db_connection = util.open_db_connection()
            cur = db_connection.cursor()

            cur.execute("select id from User where username = %s and is_unb_account = true", (username))
            db_connection.commit()
            
            user_id = None
            result = cur.fetchone()
            if result is None:
                cur.execute("insert into User(username, is_unb_account, max_storage_space) values(%s, %s, %s)", 
                    (username, True, MAX_STORAGE_SPACE))
                db_connection.commit()
                user_id = cur.lastrowid
                cur.execute("insert into Folder(name, user_id, parent_folder) values(%s, %s, %s)", ("", user_id, None))
                db_connection.commit()
            else:
                user_id = result["id"]
            cur.close()

            return user_id
        except ldap3.core.exceptions.LDAPException as ex:
            raise ZerodriveException(500, "Auth error: {}".format(str(ex)))

    # POST: login a user
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "username" in body or not "password" in body:
            raise ZerodriveException(400, "Invalid request body - missing parameter.")

        username = body["username"].strip()
        password = body["password"].strip()
        auth_type = body.get("auth_type", "").strip()

        connection = util.open_db_connection()

        try:
            user_id = None
            if auth_type == "":
                user_id = self.auth_db(username, password)
            elif auth_type == "unb":
                user_id = self.auth_ldap(username, password, self.ldap_server_unb, config.ldap_unb["use_tls"])
            elif auth_type == "dev":
                user_id = self.auth_ldap(username, password, self.ldap_server_dev, config.ldap_dev["use_tls"])
            else:
                raise ZerodriveException(400, "Unknown auth type: {}".format(auth_type))

            if user_id == None:
                raise ZerodriveException(400, "Invalid username or password.")

            cur = connection.cursor()

            # Invalidate existing session token, if it exists
            old_session_token = request.cookies.get(auth.SESSION_COOKIE_NAME)
            if old_session_token is not None:
                cur.execute("delete from Session where token = %s", (old_session_token))
                connection.commit()

            # Generate and store new session token
            session_token = os.urandom(32).hex()
            expiry_datetime = datetime.utcnow()
            expiry_datetime = expiry_datetime.replace(day=expiry_datetime.day + auth.SESSION_TOKEN_LIFETIME, microsecond=0)
            cur.execute("insert into Session(token, user_id, expiry_time) values(%s, %s, %s)", (session_token, user_id, expiry_datetime))
            connection.commit()
            cur.close()
            
            # Set session token in a cookie and return it as part of the response
            response = make_response()
            response.status_code = 200
            response.set_cookie(auth.SESSION_COOKIE_NAME,
                session_token, 
                secure=True, 
                httponly=True, 
                max_age=auth.SESSION_TOKEN_LIFETIME * 24 * 60 * 60)
            return response
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured: {}".format(err.args[1]))

    # DELETE: logout the current user
    def delete(self):
        old_session_token = request.cookies.get(auth.SESSION_COOKIE_NAME)
        if old_session_token is None:
            raise ZerodriveException(400, "User not logged in")

        connection = util.open_db_connection()
        try:
            cur = connection.cursor()
            cur.execute("delete from Session where token=%s", (old_session_token))
            connection.commit()
            cur.close()

            response = make_response()
            response.status_code = 200
            response.set_cookie(auth.SESSION_COOKIE_NAME, max_age=0)
            return response
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured: {}".format(err.args[1]))
