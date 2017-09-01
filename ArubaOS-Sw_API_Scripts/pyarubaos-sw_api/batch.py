import requests
import json
import base64
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

#commands must be bytes not str for encoding
command_bytes = b'router ospf\narea backbone\ninterface loopback 0\nip ospf all area 0'
#perform encoding
encode_command = base64.b64encode(command_bytes)
#bytes must be decoded as a utf-8 string for the dict. It is base64 but as a unicode string
command_dict = {'cli_batch_base64_encoded': encode_command.decode('utf-8')}
print(command_dict)

post_batch = requests.post(url + 'cli_batch', headers=cookie, data=json.dumps(command_dict), timeout=1)
if post_batch.status_code == 202 :
    print('Status Code: 202 Commands Accepted')
else:
    print('Warning, Status Code: {}'.format(post_batch.status_code))


