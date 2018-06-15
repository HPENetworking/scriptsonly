import requests
import json


url = 'http://192.168.2.1/rest/v3/'
creds = {'userName': 'admin', 'password': 'admin'}

s = requests.Session()
r = s.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
cookie_response = r.json()['cookie']
if r.status_code != 201:
    print('Login error, status code {}'.format(r.status_code))

cookie = {'cookie': cookie_response}
serial = requests.get(url + 'system/status', headers=cookie, timeout=1)

if serial.status_code != 200:
    print(('Error, status code {}'.format(serial.status_code)))
else:
    print("Name:", serial.json()['name'], "\t Serial Number:", serial.json()['serial_number'])

requests.delete(url + 'login-sessions', headers=cookie, timeout=1)
