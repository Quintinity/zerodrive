##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask import request, g, make_response
from flask_restful import Resource
from .auth import requires_auth
from .exceptions import ZerodriveException
from . import util
import pymysql

class Folder(Resource):

    # POST: create a new folder
    @requires_auth
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "name" in body or not "parent_folder_id" in body:
            raise ZerodriveException(400, "Invalid request body - missing parameter.")

        # TODO: ensure values have the right types
        folder_name = body["name"]
        parent_folder_id = body["parent_folder_id"]

        connection = util.open_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("select user_id from Folder where id = %s", (parent_folder_id))
            connection.commit()
            result = cursor.fetchone()

            if result is None:
                raise ZerodriveException(404, "Specified parent folder does not exist.")
            if result["user_id"] != g.user_data["id"]:
                raise ZerodriveException(401, "You don't have permission to create a folder here.")

            cursor.execute("insert into Folder(name, user_id, parent_folder) values(%s, %s, %s)", (folder_name, g.user_data["id"], parent_folder_id))
            connection.commit()
            return {"new_folder_id": cursor.lastrowid}, 200
        except pymysql.MySQLError as err:
            if err.args[0] == 1062: # Unique key error, a folder with the given name already exists in the parent folder
                raise ZerodriveException(400, "A folder with the name '{}' already exists here.".format(folder_name))
            raise ZerodriveException(500, "A database error has occurred ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

class FolderSpecific(Resource):

    # DELETE: delete a folder
    @requires_auth
    def delete(self, folder_id):
        connection = util.open_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("delete from Folder where id=%s and user_id=%s and parent_folder is not null", (folder_id, g.user_data["id"]))
            connection.commit()
            if cursor.rowcount == 0:
                raise ZerodriveException(404, "No folder with the given ID exists for the current user.")
            return 200
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()
        
    # PUT: renames a folder
    @requires_auth
    def put(self, folder_id):
        return 200 # TODO

    # GET: retrieves information about a folder and its contents
    @requires_auth
    def get(self, folder_id):
        return 200 # TODO