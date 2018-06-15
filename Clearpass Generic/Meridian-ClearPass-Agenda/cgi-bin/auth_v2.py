#!/usr/bin/env python3.4
'''
 Copyright 2016 Hewlett Packard Enterprise Development LP.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netmanfabe"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Fabien GIRAUD"]
__license__ = "Apache2"
__version__ = "2.0.0"
__maintainer__ = "Fabien GIRAUD"
__email__ = "fabien_giraud@me.com"
__status__ = "Prototype"

'''
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import json
import requests

# Global variable def
# Replace the parameters between <> with yours
global CPPMBaseURL
CPPMBaseURL = "https://<Your_CPPM_URL>"
clientID='<ClientID_defined_in_clearpass_guest_for_guest_MGMT_through_API : in my case APIGuetMgmt>'


print('Content-type: text/html')
print('')

def authenticate(username, password):


	authURI = "/api/oauth"
	headers = {'Content-Type':'application/json'}
	d={'grant_type':'password','username':str(username),'password':str(password),'client_id':clientID}

	url = CPPMBaseURL + authURI

	# Request to authenticate the guest manager and receive corresponding token (mandatory to create guest)
	data = requests.post(url,headers=headers,data=json.dumps(d)).json()
	if "access_token" in data:
		return data['access_token']
	return None


args = cgi.FieldStorage()

username = None
password = None
for i in args.keys():
	if i == "username":
		username = args[i].value
	if i == "password":
		password = args[i].value

out = {}
if username is None or password is None:
	out['error'] = "Missing Parameter"
else:
	o = authenticate(username, password)
	if o is None:
		out['error'] = "Authentication failed"
	else:
		out['token'] = o

print(json.dumps(out))

