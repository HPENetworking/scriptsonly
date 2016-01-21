# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# In OVS/Mininet 2.2.0 by default use vlan 0
# Specify correct VLAN with HP 2920 15.16.0004 and HP 5500 EI R2221P06

# Example at http://youtu.be/GUcYqpN7hvY

import argparse
import requests
import json
import urllib

# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, 
           help="Endpoint IP address", required=True)
parser.add_argument('--vlan', type=str,
           help="VLAN ID", default='0',required=True)
args = parser.parse_args()

# Read login information from file
f = open('mylogin.txt', 'r')
login = json.loads(f.readlines()[0])
f.close

# Find where endpoint is
headers = {'content-type': 'application/json', 'x-auth-token': login["token"]}
param = {"ip":args.ip, "vid":args.vlan}
url = "https://" + login["ip"]  + ":8443/sdn/v2.0/net/nodes?" + urllib.urlencode(param)

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

