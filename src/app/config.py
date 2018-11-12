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
        if type(default_val) is int:
            val = int(val)
        elif type(default_val) is bool:
            val = bool(val)
        return val

# Default configuration
db = envdict("db")
db["name"] = "zerodrive"
db["host"] = "raspberrypi"
db["port"] = 4445
db["user"] = "root"
db["password"] = "raspberry_pi_MYSQL!"  

server = envdict("server")
server["port"] = 40500
server["cert_file"] = "/home/vlad/.local/share/mkcert/localhost.pem"
server["key_file"] = "/home/vlad/.local/share/mkcert/localhost-key.pem"

ldap_dev = envdict("ldap_dev")
ldap_dev["host"] = "raspberrypi"
ldap_dev["port"] = 1389
ldap_dev["use_tls"] = False

ldap_unb = envdict("ldap_unb")
ldap_unb["host"] = "ldap-student.cs.unb.ca"
ldap_unb["port"] = 389
ldap_unb["use_tls"] = True
