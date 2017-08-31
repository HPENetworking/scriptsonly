import requests
import json
import base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = 'http://192.168.2.1/rest/v3/'
creds = {'userName': 'admin', 'password': 'admin'}
command = 'show ip route'

s = requests.Session()
r = s.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
cookie_response = r.json()['cookie']
if r.status_code != 201:
    print('Login error, status code {}'.format(r.status_code))


cookie = {'cookie': cookie_response}
c = {'cmd': command}
post_command = requests.post(url + 'cli', headers=cookie, data=json.dumps(c), timeout=1)
print(post_command.text)


if post_command.status_code != 200:
    print(('Error, status code {}'.format(post_command.status_code)))
else:
    print('Status Code: ' + str(post_command.status_code))
    response = post_command.json()['result_base64_encoded']
    decoded_r = base64.b64decode(response).decode('utf-8')
    print(decoded_r)
    print(type(decoded_r))
