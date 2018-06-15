#!/usr/bin/env python
'''
 Copyright 2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__copyright__ = "Copyright 2016, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

test connectivity to the VSD API

'''
from vspk import v3_2 as vsdk
import json
import time
# Configuring a connection to the VSD API
nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")

# Actively connecting ot the VSD API
try:
    nc.start()
except:
    print (nc)
    print type(nc.start)
    print ( dir(nc) )
nuage_user = nc.user
domain_new = "dc1"
domain = nuage_user.domains.get_first(filter="name == '%s'" % domain_new)

print ( dir(domain) )

print '-----------------------------------------------'
print domain.__dict__
print '-----------------------------------------------'

print domain.parent_id
print '-----------------------------------------------'
count = 0
zonelist = []
zones = domain.zones.get()
for zon in zones:
    print zon.name
    zonelist.append(zon.name)
    #print type(domain[count])
    count = count + 1
print zonelist
