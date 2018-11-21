##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

## DESIGN DECISIONS ##
# - No stored procedures since I didn't want to split business logic between server and database
# - Implemented server-side sessions myself instead of using Flask-Session for learning purposes
# - A flat URL structure since it's easier to describe the tree-like directory structure with
#       - File and folder IDs are globally unique, so the /folder/10 endpoint is sufficient, we don't need /user/<uid>/folder/10
# - Files and folders are stored in the database instead the filesystem, with a max file size of 100MB
#       - This keeps the metadata and data in the same place

from flask import Flask, session, redirect, url_for, g, jsonify
from flask_restful import Api
from app import util, config, auth, User, Login, Folder, FolderSpecific, File, FileSpecific, ZerodriveException
from datetime import datetime
import os

app_path = os.path.join(os.getcwd(), os.path.dirname(__file__))

# Create Flask application and initialize it
server = Flask(__name__, static_folder="static")

# Custom exception handler
@server.errorhandler(ZerodriveException)
def on_exception(exception):
    # Log all 500 (server) errors
    if exception.code >= 500:
        print("[ERROR] {}".format(exception.message), flush=True)
    return jsonify({"message": exception.message}), exception.code

@server.after_request
def after_request(res):
    if "refresh_session_token" in g and g.refresh_session_token == True:
        connection = util.open_db_connection()
        cursor = connection.cursor()

        expiry_datetime = datetime.utcnow()
        expiry_datetime = expiry_datetime.replace(day=expiry_datetime.day + auth.SESSION_TOKEN_LIFETIME, microsecond=0)
        cursor.execute("update Session set expiry_time=%s where token=%s", (expiry_datetime, g.session_token))
        connection.commit()

        res.set_cookie(auth.SESSION_COOKIE_NAME, g.session_token, secure=True, httponly=True, max_age=auth.SESSION_TOKEN_LIFETIME * 24 * 60 * 60)
    return res

# Close any database connection after any request ends
@server.teardown_appcontext
def cleanup_after_request(a):
    if "db" in g:
        g.db.close()

# Add resource endpoints
api = Api(server)
api.add_resource(User, "/user")
api.add_resource(Login, "/login")
api.add_resource(Folder, "/folder")
api.add_resource(FolderSpecific, "/folder/<int:folder_id>")
api.add_resource(File, "/file")
api.add_resource(FileSpecific, "/file/<int:file_id>")

# Serve index.html as a fallback route, which enables the Single Page Application
@server.route("/", defaults = {"path": ""})
@server.route("/<path:path>")
def serve_static(path):
    return server.send_static_file("index.html")

if __name__ == "__main__":
    server.config["PROPAGATE_EXCEPTIONS"] = True
    server.run(
        host=config.server["host"],
        port=config.server["port"], 
        ssl_context=(config.server["cert_file"], config.server["key_file"]), 
        debug=False)