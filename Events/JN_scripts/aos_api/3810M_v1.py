import requests
import simplejson
import json

#login url
login_url = 'http://10.150.0.1:80/rest/v1/login-sessions'

#username password
login_payload = {'userName': 'ctrask', 'password': 'timshel'}

#legacy login
#l = requests.post(login_url, data=json.dumps(login_payload))

#login
#l = requests.post(login_url, json=login_payload)
#print l.text
system_url = 'http://10.150.0.1:80/rest/v1/system/status'
system_get = requests.get(system_url)
system_result = system_get.json()

#print device name
print "DEVICE:", system_result['name']
#url to get vlans
vlan_url = 'http://10.150.0.1:80/rest/v1/vlans'

#get vlan data
vlan_get = requests.get(vlan_url)
vlan_result = vlan_get.json()

#pull out list with required vlan info
vlan_dict = vlan_result.values()[1]

#print result_dict

#loop over list to scrap vlan and name
for x in vlan_dict:
    print "VLAN:", x['vlan_id']
    print "VLAN NAME:", x['name']
    print "----------------"




#for x in result.values()[1]:
#    print x

#for x in result.values():
#    print x

#for name in result.vlan_element:
#    print name

