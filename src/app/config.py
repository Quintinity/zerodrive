##########################################
# ZeroDrive - a cloud storage webapp     #
# INFO 3103 Term Project                 #
# by Vlad Marica (3440500)               #
# Fall 2018                              #
##########################################

# Default configuration. Change this for every machine if required, but don't commit changes..
# git update-index --assume-unchanged src/app/config.py

import os

# Environment variable backed dictionary
# When looking up a key, it checks if a matching environment variable
# named "ZERODRIVE_<dict name>_<key>" exists. If so, it returns the environment
# variable's value, otherwise it uses the default value in the dict.
class envdict(dict):
    def __init__(self, name):
        dict.__init__(self)
        self.name = name

    def __getitem__(self, key):
        env_var_name = "zerodrive_{}_{}".format(self.name, key).upper()
        default_val = dict.__getitem__(self, key)
        val = os.environ.get(env_var_name, default_val)
        if default_val is int:
            val = int(val)
        return val

# Default configuration
db = envdict("db")
db["name"] = "zerodrive"
db["host"] = "localhost"
db["port"] = 4445
db["user"] = "user"
db["password"] = "password"

server = envdict("server")
server["port"] = 40500
