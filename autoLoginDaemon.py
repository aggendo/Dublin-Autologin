import daemon
import time
import login as Login
import config as cfg


def run():
    with daemon.DaemonContext():
        do_something()

if __name__ == "__main__":
    config = cfg.config()
    Username = config.get_username()  # read these from the config file
    Password = config.get_password()
    if config.get_username() == "blahname":
        print(
        "this script has been run for the first time or the config has not been edited, please edit config.cfg and enter the correct things")
        exit(1)
    run()