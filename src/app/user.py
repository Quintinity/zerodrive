##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask_restful import Resource
from flask import request
from hashlib import sha256
from . import util
import pymysql
import os

MAX_STORAGE_SPACE = 500 * pow(2, 20) # Given every new account 500 MB of storage space

class User(Resource):
    def get(self):
        pass

    # POST: create a new user account
    def post(self):
        body = request.get_json()
        if not "email" in body or not "password" in body:
            return {"error": "Missing parameter in body."}, 400

        email = body["email"].strip()
        password = body["password"].strip()
        if len(email) == 0:
            return {"error": "Invalid email address."}, 400
        if len(password) == 0:
            return {"error": "Password does not meet requirements."}, 400

        salt = os.urandom(24).hex() # Our salts are 48 byte random strings
        hashpw = sha256((password + salt).encode("UTF-8")).digest().hex() # TODO: One of the deployment servers doesn't have bcrypt

        try:
            connection = util.open_db_connection()
            cur = connection.cursor()
            query = "insert into User(email, hashpw, salt, max_storage_space) values(%s, %s, %s, %s)"
            cur.execute(query, (email, hashpw, salt, MAX_STORAGE_SPACE))
            connection.commit()
            cur.close()
        except pymysql.MySQLError as err:
            code = err.args[0]
            if code == 1062:
                return {"error": "Email address already in use."}, 400
            return {"error": "A database error has occurred ({}).".format(code)}, 400

        return 200
