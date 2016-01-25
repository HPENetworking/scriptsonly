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
