##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask import request, g, make_response, send_file
from flask_restful import Resource
from .auth import requires_auth
from .exceptions import ZerodriveException
from . import util, folder
import pymysql, io

BYTES_PER_MB = pow(2, 20)
MAX_FILE_SIZE = 100 * BYTES_PER_MB # Files cannot be larger than 100 MB

def validate_file(file_data):
    if file_data is None:
        raise ZerodriveException(404, "File not found.")
    if file_data["user_id"] != g.user_data["id"]:
        raise ZerodriveException(401, "You don't have permission to access this file.")


class File(Resource):

    # POST: uploads a file to a specified folder
    @requires_auth
    def post(self):
        if not "parent_folder" in request.form:
            raise ZerodriveException(400, "Missing parent_folder field in multiform data")

        if not "file" in request.files:
            raise ZerodriveException(400, "Missing file field in multiform data")

        parent_folder_id = request.form["parent_folder"]
        connection = util.open_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("select user_id from Folder where id = %s", (parent_folder_id))
            connection.commit()
            folder_info = cursor.fetchone()
            folder.validate_folder(folder_info)

            file = request.files["file"]
            data = file.stream.read()

            if len(data) > MAX_FILE_SIZE:
                raise ZerodriveException(403, "File too large - the max allowed filesize is {}MB".format(MAX_FILE_SIZE / BYTES_PER_MB))

            cursor.execute("insert into File(name, user_id, parent_folder, data, size_bytes) values(%s, %s, %s, %s, %s)",
                (file.filename, g.user_data["id"], parent_folder_id, data, len(data)))
            connection.commit()
            return {"new_file_id": cursor.lastrowid}, 200
        except pymysql.MySQLError as err:
            if err.args[0] == 1062:
                raise ZerodriveException(403, "A file with that name already exists in this folder")
            raise ZerodriveException(500, "A database error has occured ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

class FileSpecific(Resource):
    
    # GET: download a file
    @requires_auth
    def get(self, file_id):
        connection = util.open_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("select name, user_id, data from File where id=%s", (file_id))
            connection.commit()
            file_info = cursor.fetchone()
            validate_file(file_info)

            return send_file(io.BytesIO(file_info["data"]), as_attachment=True, attachment_filename=file_info["name"])
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

    @requires_auth
    def put(self, file_id):
        body = request.get_json(silent=True)
        if body is None or not "new_file_name" in body:
            raise ZerodriveException(400, "Missing request parameter - 'new_file_name'")

        if len(body["new_file_name"]) == 0:
            raise ZerodriveException(400, "File name cannot be empty")

        connection = util.open_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("select user_id from File where id=%s", (file_id))
            connection.commit()
            file_info = cursor.fetchone()
            validate_file(file_info)

            cursor.execute("update File set name=%s where id=%s", (body["new_file_name"], g.user_data["id"]))
            connection.commit()
            return 200
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()

    @requires_auth
    def delete(self, file_id):
        connection = util.open_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("select user_id from File where id=%s", (file_id))
            connection.commit()
            file_info = cursor.fetchone()
            validate_file(file_info)

            cursor.execute("delete from File where id=%s and user_id=%s", (file_id, g.user_data["id"]))
            connection.commit()
            return 200
        except pymysql.MySQLError as err:
            raise ZerodriveException(500, "A database error has occured ({}): {}".format(err.args[0], err.args[1]))
        finally:
            cursor.close()