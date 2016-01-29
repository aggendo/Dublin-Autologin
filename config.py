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
            self.path = os.path.join(path, 'config.cfg') #custom config dir
        else:
            self.path = 'config.cfg'
        self.config = ConfigParser.ConfigParser()
        if not os.path.exists(self.path):
            logging.debug("generating config file")
            self.generate_cfg()
        self.config.readfp(open(self.path))

    def get_password(self):
        return(self.config.get("Credentials", "password"))

    def get_username(self):
        return(self.config.get("Credentials", "username"))

    def get_interval(self):
        return(self.config.get("Settings", "interval")) #has a unit at the end so no int

    def is_auto_generated(self):
        return(self.config.get("Settings", "run wizard"))

    def set_wizard_ran(self):
        self.config.set("Settings", "run wizard", '0')
        self.write_out()

    def set_username(self, name):
        self.config.set("Credentials", "username", name)
        self.write_out()

    def set_password(self, password):
        self.config.set("Credentials", "password", password)
        self.write_out()

    def write_out(self):
        self.config.write(open(self.path, "w"))

    def generate_cfg(self):
        self.config.add_section("Credentials")
        self.config.set("Credentials", "username", "blahname")
        self.config.set("Credentials", "password", "blahpass")
        self.config.add_section("Settings")
        self.config.set("Settings", "interval", "1hr")
        self.writeout()
d = config()
