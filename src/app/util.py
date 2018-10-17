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
            print("Host: {}, Port: {}, Name: {}, User: {}".format(cfg.db["host"], cfg.db["port"], cfg.db["name"], cfg.db["user"]))
            flask.g.db = pymysql.connect(host=cfg.db["host"], port=cfg.db["port"], user=cfg.db["user"], password=cfg.db["password"], db=cfg.db["name"])
        except pymysql.MySQLError as err:
            print(err.args[1])
            return None
        except Exception as err:
            print(err)
    return flask.g.db