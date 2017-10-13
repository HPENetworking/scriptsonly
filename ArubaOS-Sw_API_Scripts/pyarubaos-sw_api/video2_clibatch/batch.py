
import requests
import json
import base64
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = 'http://192.168.2.1/rest/v3/'
creds = {'userName': 'admin', 'password': 'admin'}

s = requests.Session()
r = s.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
cookie_response = r.json()['cookie']
if r.status_code != 201:
    print('Login error, status code {}'.format(r.status_code))
cookie = {'cookie': cookie_response}


#commands string
commands = 'router ospf\nenable\narea backbone\ninterface loopback 0\nip address 1.1.1.1\nip ospf all area 0'
#commands must be bytes not a string
command_bytes = commands.encode()
#perform encoding to base64
base64_command = base64.b64encode(command_bytes)
#bytes must be decoded as a utf-8 string for the dict. It is base64 but as a unicode string
command_dict = {'cli_batch_base64_encoded': base64_command.decode('utf-8')}


post_batch = requests.post(url + 'cli_batch', headers=cookie, data=json.dumps(command_dict), timeout=1)
if post_batch.status_code == 202 :
    print('Status Code: 202 Commands Accepted')
    ospf_verify = {'cmd': 'show ip ospf interface'}
    time.sleep(0.5)
    verify = requests.post(url + 'cli', headers=cookie, data=json.dumps(ospf_verify), timeout=1)
    verify_response = verify.json()['result_base64_encoded']
    decoded_r = base64.b64decode(verify_response).decode('utf-8')
    print(decoded_r)
else:
    print('Warning, Status Code: {}'.format(post_batch.status_code))


