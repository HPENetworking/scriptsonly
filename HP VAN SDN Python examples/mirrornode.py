# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Example of single switch port mirroring

# OUTPUT NORMAL + OUTPUT PORT works with OVS/Mininet
# Not supported with HP 2920 as of 15.16.0004
#     or HP 5500 EI R2221P06
#
# For HW-based devices you currently need to specify output ports
# within rule (no packet SDN-configured packet replication 
# together with local control plane)

# Mininet: Run ping: "h1 ping h2 &". Start dump on analyzer 
# with "h3 tcpdump -l icmp". You should not see any ICMP traffic 
# on h3 until you enable port mirroring (h1 mirror, h3 monitor).

# Example at http://youtu.be/7YA25HXkHtw

import argparse
import requests
import json
import urllib
import sys

# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument('--mirror', type=str, 
           help="Node to be mirrored IP address", required=True)
parser.add_argument('--monitor', type=str,
           help="Analyzer IP address", required=True)
parser.add_argument('--timeout', type=int,
           help="Flow hard timeout (default 60)", required=False, default=60)
args = parser.parse_args()

# Read login information from file
f = open('mylogin.txt', 'r')
login = json.loads(f.readlines()[0])
f.close

# Find where endpoints are
headers = {'content-type': 'application/json', 'x-auth-token': login["token"]}
url = "https://" + login["ip"]  + ":8443/sdn/v2.0/net/nodes"

r = requests.get(url, verify=False, headers=headers)

# Get port and DPID information about mirror and monitor
mirrorDpid=""
monitorDpid=""
for node in r.json()["nodes"]:
   if node["ip"]==args.mirror:
       mirrorPort = node["port"]
       mirrorDpid = node["dpid"]
   if node["ip"]==args.monitor:
       monitorPort = node["port"]
       monitorDpid = node["dpid"]

# Exit if not found or not on the same switch
if mirrorDpid != monitorDpid or mirrorDpid == "":
   print "Monitor and mirror not on the same switch or not found. Exiting."
   sys.exit() 

# Prepare rule with OUTPUT NORMAL + OUTPUT monitorPort
flow = {"flow":{
    "priority":50000,
    "hard_timeout":args.timeout,
    "match":[{"in_port":mirrorPort}],
    "instructions":[{"apply_actions":
    [{"output":monitorPort},{"output":0xfffffffa}]}]
    }}

flowurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows") 

fr = requests.post(flowurl, data=json.dumps(flow), 
     headers=headers,verify=False) 

if (fr.status_code == 201):
    print "Success !"
else: print "ERROR: " + fr.content
