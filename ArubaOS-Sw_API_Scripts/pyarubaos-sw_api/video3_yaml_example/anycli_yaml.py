"""A script to demonstrate using the anycli feature in ArubaOS-Switch 16.04.
This example utilises import of data from a local YAML file
This script is aimed at those with little python experience, the lack of functions is intentional.
Example YAML file for import: anycli_yaml.yaml
"""
import requests
import json
import base64
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open("anycli_yaml.yaml", 'r') as stream:
    try:
        yaml_data = yaml.load(stream)
        ip_addr = yaml_data['ip_addr']
        username = yaml_data['username']
        password = yaml_data['password']
        command = yaml_data['command']
    except yaml.YAMLERROR as exc:
        print(exc)


url = 'https://{}/rest/v3/'.format(ip_addr)
creds = {'userName': username, 'password': password}

s = requests.Session()
r = s.post(url + 'login-sessions', json=creds, timeout=3, verify=False)
cookie_response = r.json()['cookie']
if r.status_code != 201:
    print('Login error, status code {}'.format(r.status_code))


cookie = {'cookie': cookie_response}
c = {'cmd': command}
post_command = requests.post(url + 'cli', headers=cookie, json=c, timeout=3, verify=False)

if post_command.status_code != 200:
    print(('Error, status code {}'.format(post_command.status_code)))
else:
    response = post_command.json()['result_base64_encoded']
    decoded_r = base64.b64decode(response).decode('utf-8')
    print(decoded_r)

logout = requests.delete(url + 'login-sessions', headers=cookie, verify=False)
if logout.status_code == 204:
        print("Logged out!", logout.status_code)
else:
    print("Logout is not successful", logout.status_code)
