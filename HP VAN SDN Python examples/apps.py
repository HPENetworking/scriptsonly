# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Just to test connectivity - prints apps installed on controller

import argparse
import requests
import json

# Read login information from file
f = open('mylogin.txt', 'r')
login = json.loads(f.readlines()[0])
f.close

# Read installed apps
headers = {'content-type': 'application/json', 'x-auth-token': login["token"]}
url="https://" + login["ip"]  + ":8443/sdn/v2.0/apps"

r = requests.get(url, verify=False, headers=headers)

print "Installed apps:"
print "---------------"
for record in r.json()['apps']:
   print record['name']
