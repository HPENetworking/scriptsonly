# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Enter IP address of endpoint, duration and rate. Script will create 
# new meter (no checking whether it is used or available) with defined 
# rate and drop action (rate-limit) and create rule for endpoint IP 
# (based on its location) with OUTPUT NORMAL + assign to meter

# Not implemented on OVS/Mininet 2.2.0
# Tested with HP 2920 15.16.0004 and HP 5500 EI R2221P06

# http://youtu.be/Pw6bnsf0e1Q

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
parser.add_argument('--timeout', type=int,
           help="Flow hard timeout (default 60)", required=False, default=60)
parser.add_argument('--limit', type=int,
           help="Rate-limit in kbps (default 256)", required=False, default=256)
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

# Create new meter
meter = {"version": "1.3.0",
 "meter": {
 "id": 1,
 "command": "add",
 "flags": ["kbps","burst","stats"],
 "bands": [{
 "burst_size": args.limit/2,"rate": args.limit, "mtype": "drop"}]}}

meterurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/meters")

mr = requests.post(meterurl, data=json.dumps(meter),
     headers=headers,verify=False)

if (mr.status_code == 201):
    print "Meter created !"
else: print "ERROR: " + mr.content

# Create new rule with OUTPUT NORMAL and assign meter
flow = {"flow":{
    "priority":50000,
    "hard_timeout":args.timeout,
    "match":[{"ipv4_src":args.ip},{"eth_type":"ipv4"},
             {"in_port":r.json()["nodes"][0]["port"]}],
    "instructions":[{"meter":1},
         {"apply_actions":[{"output":0xfffffffa}]}]
    }}

flowurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows") 

fr = requests.post(flowurl, data=json.dumps(flow), 
     headers=headers,verify=False) 

if (fr.status_code == 201):
    print "Success !"
else: print "ERROR: " + fr.content
