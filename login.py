import subprocess
import requests
#"fw_username=j_sandstedt&fw_password=Dublin&fw_domain=dublinschool.org&submit=Login&action=fw_logon&fw_logon_type=logon&redirect="
prename="fw_username="
prepass="&fw_password="
footer="&fw_domain=dublinschool.org&submit=Login&action=fw_logon&fw_logon_type=logon&redirect="
#url = 'https://192.168.23.1:4100/wgcgi.cgi'
url = 'https://192.168.23.1:4100/wgcgi.cgi'#'http://192.168.23.1:4100'#/wgcgi.cgi'
Uport=4100
Verify=False
match="./auth_portal/Default/logo" #log for in failed

###USER SETTINGS####
Username="blah my username is here without @dublinschool.org"
Password="blah my password is here"
###END OF USER SETTINGS###

#Connection-specific DNS Suffix  . :
def attempt_login():
    Data= {'fw_username':Username,'fw_password':str(Password),
           'fw_domain': 'dublinschool.org', 'submit': 'Login',
           'action':'fw_logon', 'fw_logon_type':'logon',
           'redirect':""}
    req = requests.post(url, data=Data, verify=Verify)#prename+Username+prepass+str(Password)+footer)
    #print(req.text)
    #response = urllib2.urlopen(req)
    #the_page = response.read()
    #print(the_page)
attempt_login()

#here is some trickery to work in windows
startupinfo = None
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
proc = subprocess.Popen(command, startupinfo=startupinfo)
output = subprocess.Popen(["ipconfig", "/all"], stdout=subprocess.PIPE).communicate()[0]

#print output
for line in output.split('\n'):
    if line.startswith('   Connection-specific DNS Suffix  . : '):
        if not len(line)==40:
            line=line[39:]
            print(line)
            if "dublinschool.org" in line:
                print('found')
