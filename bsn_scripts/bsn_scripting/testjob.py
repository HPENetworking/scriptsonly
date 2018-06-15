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

Flask script that auto provisions HPE DCN
08232016 Initial release. This script will generate a new (tenant), a new domain and
add zones, subnets and default ACL rules for ingress and egress traffic. They default to open.



'''

from vspk import v3_2 as vsdk
import time
import ipaddress
import json
# Configuring a connection to the VSD API
nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")

# Actively connecting ot the VSD API
nc.start()

# Root User
nuage_user = nc.user
dom_new = 'Ware'
# Assuming import of vsdk, connected to the API as the nc variable
domain = nuage_user.domains.get_first(filter="name == '%s'" % dom_new)
print domain.name
print domain
print type(domain)

is_template = domain.is_template()
zone_class = vsdk.NUZoneTemplate if is_template else vsdk.NUZone
subnet_class = vsdk.NUSubnetTemplate if is_template else vsdk.NUSubnet
