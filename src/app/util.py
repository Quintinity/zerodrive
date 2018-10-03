##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

import os
import pymysql.cursors
import flask
from .config import db

def get_or_create_secret_key(secret_key_file_name):
    if os.path.isfile(secret_key_file_name):
        return open(secret_key_file_name, "r").read()
    else:
        key = os.urandom(24).hex()
        key_file = open(secret_key_file_name, "w")
        key_file.write(key)
        key_file.close()
        return key

def open_db_connection():
    if not "db" in flask.g:
        flask.g.db = pymysql.connect(host=db["host"], port=db["port"], user=db["user"], password=db["password"], db=db["name"])
    return flask.g.db