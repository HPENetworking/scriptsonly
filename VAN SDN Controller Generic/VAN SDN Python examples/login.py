# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# This script will get authentication token and store it together 
# with controller IP to mylogin.txt file, which is then read by all 
# other scripts. You can login just once (based on Keystone 
# configuration this will stay valid for 1 hour or more) and you 
# do not have to repeate this process with other scripts.

import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, help="Controller IP address",
    default="10.10.10.201")
parser.add_argument('--user', type=str, help="Username", 
    default="hp")
parser.add_argument('--password', type=str, help="Password",
    default="hp")
args = parser.parse_args()

url="https://" + args.ip + ":8443/sdn/v2.0/auth"

data = {
 "login":{
 "user":args.user,
 "password":args.password,
 "domain":"sdn"
 }
}

r = requests.post(url, data=json.dumps(data), verify=False)

print("Token: " + r.json()["record"]["token"])

login = {"ip":args.ip,"token":r.json()["record"]["token"]}

f = open('mylogin.txt', 'w')
f.write(json.dumps(login))
f.close


