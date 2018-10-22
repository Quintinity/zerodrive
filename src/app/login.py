##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################
from flask_restful import Resource
from flask import request, make_response
from hashlib import sha256
from . import util
import pymysql
import os
import secrets

__SESSION_COOKIE_NAME = "session"

class Login(Resource):
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "email" in body or not "password" in body:
            return {"error": "Missing parameter in body."}, 400

        email = body["email"].strip()
        password = body["password"].strip()

        connection = util.open_db_connection()
        try:
            cur = connection.cursor()
            cur.execute("select user_id, email, hashpw, salt from User where email = %s", (email))

            # Validate credentials
            result = cur.fetchone()
            if result is None:
                return {"error": "Invalid username or password."}, 400
            user_id = result["user_id"]
            given_hashpw = sha256((password + result["salt"]).encode("UTF-8")).digest().hex()
            if given_hashpw != result["hashpw"]:
                return {"error": "Invalid username or password."}, 400

            # Invalidate existing session token, if it exists
            old_session_token = request.cookies.get(__SESSION_COOKIE_NAME)
            if old_session_token is not None:
                cur.execute("delete from Session where token = %s", (old_session_token))

            # Generate and store new session token
            session_token = secrets.token_urlsafe()
            cur.execute("insert into Session(token, user_id) values(%s, %s)", (session_token, user_id))
            cur.close()
            
            response = make_response()
            response.status_code = 200
            response.set_cookie(__SESSION_COOKIE_NAME, session_token, secure=True, httponly=True)

            return response

        except pymysql.MySQLError:
            return {"error": "A database error has occured."}, 500

    def delete(self):
        old_session_token = request.cookies.get(__SESSION_COOKIE_NAME)
        if old_session_token is None:
            return {}, 400

        connection = util.open_db_connection()
        try:
            cur = connection.cursor()
            cur.execute("delete from Session where token=%s", (old_session_token))
            cur.close()

            response = make_response()
            response.status_code = 200
            response.set_cookie(__SESSION_COOKIE_NAME, expires=0)
            return response
            
        except pymysql.MySQLError:
            return {"error": "A database error has occured."}, 500
