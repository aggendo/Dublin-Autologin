import subprocess
import requests
from sys import platform as OSName
from os import name as SYSPlat
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
url = 'https://192.168.23.1:4100/wgcgi.cgi'
Uport=4100
Verify=False
match="./auth_portal/Default/logo" #look for in responce to see if login failed.

###USER SETTINGS####
Username="blah username here" #no @dublinschool.org
Password="blah password here"
###END OF USER SETTINGS###

#Connection-specific DNS Suffix  . :
def attempt_login():
    Data= {'fw_username':Username,'fw_password':str(Password),
           'fw_domain': 'dublinschool.org', 'submit': 'Login',
           'action':'fw_logon', 'fw_logon_type':'logon',
           'redirect':""}
    req = requests.post(url, data=Data, verify=Verify)#prename+Username+prepass+str(Password)+footer)
    #print(req.text)
    if(match in req.text): #login failed
        

def checkwifi():
    #here is some trickery to work in windows
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
        pass #TODO: Linux code here

if(__name__=="__main__"):
    checkwifi()
