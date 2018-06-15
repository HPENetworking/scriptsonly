import requests

vlan_number = input('Enter VLAN number:')
vlan_name = input('Enter VLAN name:')

url_login = "http://192.168.1.29/rest/v1/login-sessions"
url_vlans = "http://192.168.1.29/rest/v1/vlans"

payload_login = "{\"userName\": \"joe\", \"password\": \"x\"}"

get_cookie = requests.request("POST", url_login, data=payload_login)

r_cookie = get_cookie.json()['cookie']

print(r_cookie)

payload_vlan = "{\"vlan_id\":"+vlan_number+",\"name\":\""+vlan_name+"\"}"

print(payload_vlan)

headers = {'cookie': r_cookie }

config_vlan = requests.request("POST", url_vlans, data=payload_vlan, headers=headers)

print(config_vlan)

