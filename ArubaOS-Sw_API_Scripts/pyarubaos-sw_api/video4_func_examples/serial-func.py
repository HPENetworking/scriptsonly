import requests
import json


def login():
    r = requests.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
    cookie = {'cookie': r.json()['cookie']}
    if r.status_code != 201:
        print('Login error, status code {}'.format(r.status_code))
    return cookie


def get_serial(c):
    serial = requests.get(url + 'system/status', headers=c, timeout=1)
    if serial.status_code != 200:
        print(('Error, status code {}'.format(serial.status_code)))
    else:
        print("Name:", serial.json()['name'], "\t Serial Number:", serial.json()['serial_number'])


def logout(c):
    end_session = requests.delete(url + 'login-sessions', headers=c, timeout=1)
    if end_session.status_code != 204:
        print("Log out error")
    else:
        return end_session.status_code


url = 'http://192.168.2.1/rest/v3/'
creds = {'userName': 'admin', 'password': 'admin'}


c = login()
get_serial(c)
logout(c)

url = 'http://192.168.2.2/rest/v3/'

c = login()
get_serial(c)
logout(c)
