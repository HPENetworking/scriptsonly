"""A script to demonstrate using the anycli feature on multiple devices.
This example utilises import of data from a local YAML file.
This script is aimed at those with little python experience, the lack of functions is intentional.
Example YAML file for import: multi_anycli_yaml.yaml
"""
import requests
import json
import base64
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

with open("multi_anycli_yaml.yaml", 'r') as stream:
    try:
        yaml_data = yaml.load(stream)
        ip_addr = yaml_data['ip_addr']
        username = yaml_data['username']
        password = yaml_data['password']
        command = yaml_data['command']
    except yaml.YAMLERROR as exc:
        print(exc)


for switch in ip_addr:
    url = 'http://' + switch + '/rest/v3/'
    creds = {'userName': username, 'password': password}
    s = requests.Session()
    r = s.post(url + 'login-sessions', data=json.dumps(creds), timeout=1)
    cookie_response = r.json()['cookie']
    if r.status_code != 201:
        print('Login error, status code {}'.format(r.status_code))

    cookie = {'cookie': cookie_response}
    c = {'cmd': command}
    post_command = requests.post(url + 'cli', headers=cookie, data=json.dumps(c), timeout=1)

    if post_command.status_code != 200:
        print(('Error, status code {}'.format(post_command.status_code)))
    else:
        print('Status Code: ' + str(post_command.status_code))
        response = post_command.json()['result_base64_encoded']
        decoded_r = base64.b64decode(response).decode('utf-8')
        print(decoded_r)
        print('*' * 80)

