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

# Configuring a connection to the VSD API
nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")

# Actively connecting ot the VSD API
nc.start()
print ('Auth success')

# Root User


domain = nc.user.domains.get_first(filter='name == "Tower"')
if not domain:
    print('Error: Domain can not be found')
    sys.exit(-1)

print('Domain: %s' % domain.name)
for cur_zone in domain.zones.get():
    print('|-Zone: %s' % cur_zone.name)
    for cur_subnet in cur_zone.subnets.get():
        print('  |-Subnet: %s - %s - %s' % (cur_subnet.name,cur_subnet.address,cur_subnet.netmask))

print('Policies')
for cur_acl in domain.ingress_acl_templates.get():
    print('|-Ingress ACL: %s' % cur_acl.name)
    for cur_rule in cur_acl.ingress_acl_entry_templates.get():
        print('  |-Rule: %s' % cur_rule.description)

for cur_acl in domain.egress_acl_templates.get():
    print('|-Egress ACL: %s' % cur_acl.name)
    for cur_rule in cur_acl.egress_acl_entry_templates.get():
        print('  |-Rule: %s' % cur_rule.description)
