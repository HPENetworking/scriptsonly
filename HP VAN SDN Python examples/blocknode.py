# Example Python script to work with HP VAN SDN controller 2.4.5
# Tomas Kubica

# Enter IP address of endpoint to be blocked and hard timeout. 
# Script will instal rule with empty action-list (drop rule). 
# Aftewards script print flow statistics (blocked packets and bytes)
# in real time. 
 
# Tested with OVS/Mininet 2.2.0, 
# HP 2920 15.16.0004 and HP 5500 EI R2221P06
 
# Example at http://youtu.be/d4znVrp09NU 

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

# Preapare rule with empty instructions (drop traffic)
flow = {"flow":{
    "priority":50000,
    "hard_timeout":args.timeout,
    "cookie":1234,
    "flow_mod_flags":["send_flow_rem"],
    "match":[{"ipv4_src":args.ip},{"eth_type":"ipv4"},
             {"in_port":r.json()["nodes"][0]["port"]}],
    "instructions":[{"apply_actions":[]}]
    }}

blockurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows") 

br = requests.post(blockurl, data=json.dumps(flow), 
     headers=headers,verify=False) 

if (br.status_code == 201):
    print "Success !"
else: 
    print "ERROR: " + br.content
    sys.exit()

# Read flow stats
statsparam = {"cookie":1234}
statsurl = ("https://" + login["ip"]
     + ":8443/sdn/v2.0/of/datapaths/"
     + r.json()["nodes"][0]["dpid"] + "/flows?"
     + urllib.urlencode(statsparam))
print "Flow statistics. Press CTRL+C to exit."

# Do this while rule exist (have not time out yet)
exist = True
try:
    while exist:
       sr = requests.get(statsurl, headers=headers,verify=False)
       exist = False;
       for stat in sr.json()["flows"]:
		   # Is there rule with our cookie?
           if stat["cookie"] == "0x1234":
               packets = stat["packet_count"]
               bytes = stat["byte_count"]
               duration = str(stat["duration_sec"])
               output = "Matched " + packets + " packets and " + bytes \
                  + " bytes for " + duration + " seconds"
               # This is alternative to simply print to rewrite lines
               sys.stdout.write('%s\r' % output)
               sys.stdout.flush()
               exist = True
       # We will check only once per second
       time.sleep(1)
# Catch CTRL+C
except KeyboardInterrupt:
    print "\nExiting\n"    
    pass

print "\nRule no longer exist\n"
