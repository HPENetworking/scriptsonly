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
   
__author__ = "Pack3tL0ss"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Wade Wells"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Wade Wells"
__status__ = "Prototype"

This script queries the status of a client on the aruba controller via the XML api.
It queries the user and sets the 'status' variable based on the online status of the user
status will be True if online and False if not.

Example use Case and the exact reason it was scripted.  My GarageDoor controller (my Fork on github) will send images
anytime my garage door is opened.  My controller code imports and calls this function to first determine if
my mobile device is online (on the wireless).  If it is then I am home, and it does not send an image.  If my mobile
is offline (which means I'm away from the house) then it sends the images.  

Some configuration is required on the controller to allow an api query from a device, and set the secret.  I also have 
a reference to the certificate to use in the query request which just prevents an error.  Setting verify=False should work 
with the self-signed certificate (but will print a security warning to the console).
'''
import requests
import xml.etree.ElementTree as ET

debug = False
    
def userquery():    
        # Debugging for python requests
        if debug:
            import logging
    
            # Setup Debug Logging
            try:
                import http.client as http_client
            except ImportError:
                # Python 2
                import httplib as http_client
    
                http_client.HTTPConnection.debuglevel = 1
    
            ### You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
    
        # Request Payload query user status on Aruba Controller
        data = """xml=<aruba command=\"user_query\">
        <name>stan</name>
        <authentication>cleartext</authentication>
        <key>secret</key>
        <version>1.0</version>
        </aruba>
        """
    
        headers = {'Content-Type': 'text/xml', 'Accept': '*/*'}  # set what your server accepts
        r = requests.post('https://mc1.home.lab/auth/command.xml', headers=headers, data=data, verify='/home/pi/garage-door-controller/api/wadelab1ca.cer')
        root = ET.fromstring(r.content)
    
        status = root.find('status').text
    
        if status == 'Error':
            return False
        elif status == 'Ok':
            return True
        else:
            return LookupError

if __name__=='__main__':
   print userquery()
