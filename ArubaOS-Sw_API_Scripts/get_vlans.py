import requests
import pprint

url = 'http://192.168.1.29/rest/v1/vlans'

get_vlans = requests.get(url)

get_vlans_json = get_vlans.json()

#print(type(get_vlans_json))

#pprint.pprint(get_vlans_json)

elements = get_vlans_json['vlan_element']

print("2930 VLANS:")

for x in elements:
   print("VLAN: {0} \t NAME: {1}".format(x['vlan_id'], x['name']))



