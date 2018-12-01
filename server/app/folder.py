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
import pymysql, json

def validate_folder(query_results):
    if query_results is None:
        raise ZerodriveException(404, "Specified folder does not exist.")
    if query_results["user_id"] != g.user_data["id"]:
        raise ZerodriveException(401, "You don't have permission to do this operation..")

class Folder(Resource):

    # POST: create a new folder
    @requires_auth
    def post(self):
        body = request.get_json(silent=True)
        if body is None or not "name" in body or not "parent_folder_id" in body:
            raise ZerodriveException(400, "Invalid request body - missing parameter.")

        folder_name = body["name"]
        parent_folder_id = body["parent_folder_id"]

        if len(folder_name) == 0:
            raise ZerodriveException(400, "Folder name cannot be empty")

        connection = util.open_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("select user_id from Folder where id = %s", (parent_folder_id))
            connection.commit()
            result = cursor.fetchone()

            validate_folder(result)

            cursor.execute("insert into Folder(name, user_id, parent_folder) values(%s, %s, %s)", (folder_name, g.user_data["id"], parent_folder_id))
            connection.commit()
            return {"new_folder_id": cursor.lastrowid}, 200
        except pymysql.MySQLError as err:
            if err.args[0] == 1062: # Unique key error, a folder with the given name already exists in the parent folder
                raise ZerodriveException(400, "A folder named '{}' already exists here.".format(folder_name))
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
            cursor.execute("select user_id, parent_folder from Folder where id=%s", (folder_id))
            connection.commit()
            folder_info = cursor.fetchone()

            # Check info to see if we can actually delete this folder
            validate_folder(folder_info)
            if folder_info["parent_folder"] is None:
                raise ZerodriveException(401, "You cannot delete your root folder.")
                
            cursor.execute("delete from Folder where id=%s", (folder_id))
            connection.commit()
            return 200
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()
        
    # PUT: renames a folder
    @requires_auth
    def put(self, folder_id):
        body = request.get_json(silent=True)
        if body is None or not "name" in body:
            raise ZerodriveException(400, "Invalid request body - missing 'name' parameter.")

        new_name = body["name"]
        if len(new_name) == 0:
            raise ZerodriveException(400, "Invalid folder name.")

        connection = util.open_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("select user_id from Folder where id=%s", (folder_id))
            connection.commit()
            folder_info = cursor.fetchone()

            validate_folder(folder_info)

            cursor.execute("update Folder set name=%s where id=%s", (new_name, folder_id))
            connection.commit()
        except pymysql.MySQLError as err:
            # TODO: specifically handle unique key failures (non-unique names in parent folder)
            raise ZerodriveException(500, "A database error has occurred ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

    # GET: retrieves information about a folder and its contents
    @requires_auth
    def get(self, folder_id):

        connection = util.open_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("select name, user_id, parent_folder, last_modified from Folder where id=%s", (folder_id))
            connection.commit()
            folder_info = cursor.fetchone()
            validate_folder(folder_info)

            # The version of MariaDB using on the info3103 server is old and doesn't support recursive queries
            # So I have to do this in order to build up the hierarchy
            hierarchy = []
            parent_folder = folder_info["parent_folder"]
            while parent_folder is not None:
                cursor.execute("select name, parent_folder from Folder where id=%s", (parent_folder))
                connection.commit()
                result = cursor.fetchone()
                hierarchy.insert(0, {"name": result["name"], "id": parent_folder})
                parent_folder = result["parent_folder"]

            cursor.execute("select id, name, null as size_bytes, 'Folder' as type, last_modified from Folder where parent_folder=%s union \
                            select id, name, size_bytes, 'File' as type, last_modified from File where parent_folder=%s", (folder_id, folder_id))
            connection.commit()
            contents = cursor.fetchall()

            return {
                "name": folder_info["name"],
                "id": folder_id,
                "last_modified": folder_info["last_modified"],
                "hierarchy": hierarchy,
                "contents": contents
            }, 200
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occurred ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

        return 200 # TODO