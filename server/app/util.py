##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

import os
import pymysql.cursors
import flask
from . import config as cfg
from .exceptions import ZerodriveException
from json import JSONEncoder
from datetime import datetime

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
        try:
            flask.g.db = pymysql.connect(
                host=cfg.db["host"],
                port=cfg.db["port"],
                user=cfg.db["user"],
                password=cfg.db["password"], 
                db=cfg.db["name"],
                cursorclass=pymysql.cursors.DictCursor)
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured: {}".format(err.args[1]))
    return flask.g.db

class ExtendedJSONEncoder(JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime):
            return str(obj)
        return JSONEncoder.default(self, obj)
