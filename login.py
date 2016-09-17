import subprocess
import requests
from sys import platform as OSName
from os import name as SYSPlat
import logging
import time
import config as cfg
logging.basicConfig(filename='example.log',level=logging.DEBUG)
url = 'https://192.168.23.1:4100/logon.shtml'
Uport=4100
Verify=False
match="./auth_portal/Default/logo" #look for in responce to see if login failed.

config = cfg.config()
Username = config.get_username()  # read these from the config file
Password = config.get_password()
Interval = config.get_interval()

del config

def performLoginCheck():
    if Username == "blahname":
        print("this script has been run for the first time or the config has not been edited, please edit config.cfg and enter the correct things")
        exit(1)

#the following stores all the information needed to log in
Data= {'fw_username':Username,'fw_password':str(Password),
           'fw_domain': 'dublinschool.org', 'submit': 'Login',
           'action':'fw_logon', 'fw_logon_type':'logon',
           'redirect':""}
#what you send to log out of the wifi
LogOut = {'Logout':'Logout','action':'fw_logon','fw_logon_type':'logout'}

def logout():
    logging.info("attempting log out")
    req = requests.post(url, data=LogOut, verify=Verify)
    logging.info("logged out")
    print "logged out"

#Connection-specific DNS Suffix  . :
def attempt_login():
    req = requests.post(url, data=Data, verify=Verify)#prename+Username+prepass+str(Password)+footer)
    #print(req.text)
    if(match in req.text): #login failed
        logging.error("you must have set things wrong because login failed")
        exit(0)

def checkwifi():
    #here is some trickery to work in windows
    #without making a cmd window pop up frequently
    startupinfo = None
    print "os.name=="+OSName
    if OSName == 'nt' or OSName =="win32": #the user is using windows so we don't want cmd to show
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        output = subprocess.Popen(["ipconfig", "/all"], stdout=subprocess.PIPE,
                                  startupinfo=startupinfo).communicate()[0]
        e=0
        lines=output.split('\n')
        for line in lines:
            if line.startswith('   Connection-specific DNS Suffix  . : '):
                if not len(line)==40:
                    nline=line[39:]
                    print(line)
                    if "dublinschool.org" in nline:
                        if(not lines[e-3].startswith('Tunnel')): #make sure this is not a tunnel adapter
                            print('found')
                            return(True)
            e=e+1; #maybe cleanup later
    elif SYSPlat == 'linux2':
        from pythonwifi.iwlibs import Wireless
        wifi = Wireless('wlan0')
        if(wifi.getEssid()=="student"):
            return(True)
    else:
        #TODO: fix this so that it can fail if you aren't connected
        return(True)

def daemonInnerLoop():
    while true:
        attempt_login();
        time.sleep(Interval)
        #TODO: make sure you are connected to dublin internet here


if(__name__=="__main__"):
    performLoginCheck()
    if(checkwifi()):
        attempt_login()
    else:
        print("you do not seem to be connected to the network, maybe your settings are wrong?!?")
