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

from . import util
from . import auth

import pymysql, os

class Login(Resource):
    # POST: login a user
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "email" in body or not "password" in body:
            return {"error": "Missing parameter in body."}, 400

        email = body["email"].strip()
        password = body["password"].strip()

        connection = util.open_db_connection()
        if connection is None:
            return {"error": "Failed to connect to database"}, 500

        try:
            cur = connection.cursor()
            cur.execute("select id, email, hashpw, salt from User where email = %s", (email))
            connection.commit()

            # Validate credentials
            result = cur.fetchone()
            if result is None:
                return {"error": "Invalid username or password."}, 400
            user_id = result["id"]
            given_hashpw = sha256((password + result["salt"]).encode("UTF-8")).digest().hex()
            if given_hashpw != result["hashpw"]:
                return {"error": "Invalid username or password."}, 400

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
                secure=False, 
                httponly=True, 
                max_age=auth.SESSION_TOKEN_LIFETIME * 24 * 60 * 60)
            return response
        except pymysql.MySQLError as err:
            return {"error": "A database error has occured: {}".format(err.args[1])}, 500

    # DELETE: logout the current user
    def delete(self):
        old_session_token = request.cookies.get(auth.SESSION_COOKIE_NAME)
        if old_session_token is None:
            return {}, 400

        connection = util.open_db_connection()
        if connection is None:
            return {"error": "Failed to connect to database"}, 500

        try:
            cur = connection.cursor()
            cur.execute("delete from Session where token=%s", (old_session_token))
            cur.close()

            response = make_response()
            response.status_code = 200
            response.set_cookie(auth.SESSION_COOKIE_NAME, max_age=0)
            return response
            
        except pymysql.MySQLError as err:
            return {"error": "A database error has occured: {}".format(err.args[1])}, 500
