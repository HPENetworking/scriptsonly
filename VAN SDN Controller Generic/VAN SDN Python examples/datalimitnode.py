# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Implements transmit data limit for selected node. Script first 
# installs unique OUTPUT NORMAL rule with source IP and physical 
# port (based on location information in controller) in order to 
# have per source IP accounting. Script then periodically check 
# flow stats and compare transmitted bytes with limit set as 
# script argument. When node sent more data than allowed, 
# script modify existing flow with no actions (drop subsequent packets).

# Tested with OVS/Mininet 2.2.0
# Not supported on HP 2920 and 5500 EI 
#   as bytes stats are not available for HW flows

# Example at http://youtu.be/ccwPe0lfPwM

import argparse
import requests
import json
import urllib
import sys
import time

# Parse inputs
parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, 
           help="Endpoint IP address", required=True)
parser.add_argument('--vlan', type=str,
           help="VLAN ID", default='0',required=True)
parser.add_argument('--timeout', type=int,
           help="Flow hard timeout (default 60)", required=False, default=60)
parser.add_argument('--datalimit', type=int,
           help="Datalimit in bytes (default 2000)", required=False, default=2000)
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

# Install OUTPUT NORMAL rule for source IP
# Use higher priority than default rule
# We are doing this in order to have accounting data per source IP
flow = {"flow":{
    "priority":50000,
    "hard_timeout":args.timeout,
    "cookie":1234,
    "match":[{"ipv4_src":args.ip},{"eth_type":"ipv4"},
             {"in_port":r.json()["nodes"][0]["port"]}],
    "instructions":[{"apply_actions":[{"output":0xfffffffa}]}]
    }}

flowurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows") 

fr = requests.post(flowurl, data=json.dumps(flow), 
     headers=headers,verify=False) 

if (fr.status_code == 201):
    print "Success !"
else: 
    print "ERROR: " + fr.content
    sys.exit()

# We will periodically read accounting data
statsparam = {"cookie":1234}
statsurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows?"
     + urllib.urlencode(statsparam))
print "Flow statistics. Press CTRL+C to exit."

# Do this while transfered data is less than datalimit
underlimit = True
try:
    while underlimit:
       sr = requests.get(statsurl, headers=headers,verify=False)
       underlimit = False;
       for stat in sr.json()["flows"]:
           if stat["cookie"] == "0x1234":
               packets = stat["packet_count"]
               bytes = stat["byte_count"]
               duration = str(stat["duration_sec"])
               output = "Matched " + packets + " packets and " + bytes \
                  + " bytes for " + duration + " seconds"
               sys.stdout.write('%s\r' % output)
               sys.stdout.flush()
               # Are we still under limit?
               if int(bytes) < args.datalimit: underlimit = True      
       time.sleep(1)
except KeyboardInterrupt:
    print "\nExiting\n"    
    pass

print "\nOver limit\n"

# Update rule to not include action (drop traffic)
flowupdate = {"flow":{
    "priority":50000,
    "hard_timeout":args.timeout,
    "cookie":1234,
    "match":[{"ipv4_src":args.ip},{"eth_type":"ipv4"},
             {"in_port":r.json()["nodes"][0]["port"]}],
    "instructions":[]
    }}

flowurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows")

fru = requests.put(flowurl, data=json.dumps(flowupdate),
     headers=headers,verify=False)

print "Additional traffic blocked"
