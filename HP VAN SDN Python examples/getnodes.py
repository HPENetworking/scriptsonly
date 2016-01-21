# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Print end-points

import argparse
import requests
import json

# Read login information from file
f = open('mylogin.txt', 'r')
login = json.loads(f.readlines()[0])
f.close

headers = {'content-type': 'application/json', 'x-auth-token': login["token"]}
url="https://" + login["ip"]  + ":8443/sdn/v2.0/net/nodes"

r = requests.get(url, verify=False, headers=headers)

# Print nodes with formating
print('{0:15.15} {1:20.20} {2:26.26} {3:10.10}'
    .format('IP','MAC', 'Switch', 'Port'))
print('{0:15.15} {1:20.20} {2:26.26} {3:10.10}'
    .format('--','---', '------', '----'))

for record in r.json()["nodes"]:
   print('{0:15.15} {1:20.20} {2:26.26} {3:10.10}'
    .format(record["ip"],record["mac"],
    record["dpid"],str(record["port"])))

