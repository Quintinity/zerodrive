##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask import Flask, session, redirect, url_for, g
from flask_restful import Api
from app import util, config, User, Login
import os

app_path = os.path.join(os.getcwd(), os.path.dirname(__file__))

# Create Flask application and initialize it
server = Flask("zerodrive")
server.secret_key = util.get_or_create_secret_key(os.path.join(app_path, "secret.key"))

# Close any database connection after any request ends
@server.teardown_appcontext
def cleanup_after_request(a):
    if "db" in g:
        g.db.close()

# Add resource endpoints
api = Api(server)
api.add_resource(User, "/user")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    server.run(port=config.server["port"], debug=True)