import ConfigParser #TODO: this is renamed in python 3 so use try statement
import os
from os.path import join, exists
import logging

#example format:
"""
[Settings]
....
[Credentials]
username=myUsername
password=myPassword
[Info]
settingsversion=1
"""

class config:

    def __init__(self, path=None):
        if not path==None:
            path = os.path.join(path, 'config.cfg') #custom config dir
        else:
            path = 'config.cfg'
        self.config = ConfigParser.ConfigParser()
        if not os.path.exists(path):
            logging.debug("generating config file")
            self.generate_cfg(path)
        self.config.readfp(open(path))

    def get_password(self):
        return(self.config.get("Credentials", "password"))

    def get_username(self):
        return(self.config.get("Credentials", "username"))

    def get_interval(self):
        return(self.config.get("Settings", "interval")) #has a unit at the end so no int

    def generate_cfg(self, path):
        self.config.add_section("Credentials")
        self.config.set("Credentials", "username", "blahname")
        self.config.set("Credentials", "password", "blahpass")
        self.config.add_section("Settings")
        self.config.set("Settings", "interval", "1hr")
        self.config.write(open(path, "w"))
d = config()
