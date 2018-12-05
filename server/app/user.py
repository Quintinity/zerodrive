##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask_restful import Resource
from flask import request, g, make_response
from hashlib import sha256

from . import util
from .auth import requires_auth, SESSION_COOKIE_NAME
from .exceptions import ZerodriveException

import os, pymysql

MAX_STORAGE_SPACE = 10 * pow(2, 20) # Give every new account 10 MB of storage space

class User(Resource):
    # GET: retrieves information about about the current user
    # There is no way to query information about specific users since it's not needed
    @requires_auth
    def get(self):
        return g.user_data, 200

    # POST: create a new user account
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "username" in body or not "password" in body:
            raise ZerodriveException(400, "Missing parameter in body.")

        username = body["username"].strip()
        password = body["password"].strip()
        if len(username) == 0:
            raise ZerodriveException(400, "Username cannot be empty")
        if len(password) == 0:
            raise ZerodriveException(400, "Password does not meet requirements.")

        salt = os.urandom(24).hex() # Our salts are 48 byte random strings
        hashpw = sha256((password + salt).encode("UTF-8")).digest().hex() # TODO: One of the deployment servers doesn't have bcrypt

        connection = util.open_db_connection()

        try:
            cur = connection.cursor()
            query = "insert into User(username, hashpw, salt, max_storage_space) values(%s, %s, %s, %s)"
            cur.execute(query, (username, hashpw, salt, MAX_STORAGE_SPACE))
            connection.commit()
            cur.execute("insert into Folder(name, user_id, parent_folder) values(%s, %s, %s)", ("", cur.lastrowid, None))
            connection.commit()
            cur.close()
        except pymysql.MySQLError as err:
            code = err.args[0]
            if code == 1062:
                raise ZerodriveException(400, "Username is already in use.")
            raise ZerodriveException(500, "A database error has occurred ({}).".format(err.args[1]))
        return 200

    @requires_auth
    def delete(self):
        connection = util.open_db_connection()

        try:
            cur = connection.cursor()
            cur.execute("delete from User where id=%s", (g.user_data["id"]))
            connection.commit()
            cur.close()

            # Clear session cookie
            response = make_response()
            response.status_code = 200
            response.set_cookie(SESSION_COOKIE_NAME, max_age=0)
            return response
        except pymysql.MySQLError as err:
            raise ZerodriveException(400, "A database error has occurred: {}.".format(err.args[1]))
