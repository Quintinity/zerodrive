##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask import Flask, session, redirect, url_for, g, jsonify
from flask_restful import Api
from app import util, config, User, Login, Folder, FolderSpecific, ZerodriveException
import os

app_path = os.path.join(os.getcwd(), os.path.dirname(__file__))

# Create Flask application and initialize it
server = Flask("zerodrive")
server.secret_key = util.get_or_create_secret_key(os.path.join(app_path, "secret.key"))

# Custom exception handler
@server.errorhandler(ZerodriveException)
def on_exception(exception):
    # Log all 500 (server) errors
    if exception.code >= 500:
        print("[ERROR] {}".format(exception.message), flush=True)
    return jsonify({"message": exception.message}), exception.code

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

if __name__ == "__main__":
    server.config["PROPAGATE_EXCEPTIONS"] = True
    server.run(
        port=config.server["port"], 
        ssl_context=(config.server["cert_file"], config.server["key_file"]), 
        debug=False) 