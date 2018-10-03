##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

from flask_restful import Resource
from flask import request

class User(Resource):
    def post(self):
        print(request.get_json())
