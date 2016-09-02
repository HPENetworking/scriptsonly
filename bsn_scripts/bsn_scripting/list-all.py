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

test connectivity to the VSD API List all

'''
from vspk import v3_2 as vsdk

session = vsdk.NUVSDSession(
    username='csproot',
    password='csproot',
    enterprise='csp',
    api_url='https://10.132.0.126:8443'
)

session.start()

user = session.user

for cur_ent in user.enterprises.get():
    print('VMs inside Enterprise %s' % cur_ent.name)
    for cur_vm in cur_ent.vms.get():
        print('|- %s' % cur_vm.name)

    print('\nDomains inside Enterprise %s' % cur_ent.name)
    for cur_domain in cur_ent.domains.get():
        print('|- Domain: %s' % cur_domain.name)
        for cur_zone in cur_domain.zones.get():
            print('    |- Zone: %s' % cur_zone.name)
            for cur_subnet in cur_domain.subnets.get():
                print('        |- Subnets: %s - %s - %s' % (cur_subnet.name, cur_subnet.address, cur_subnet.netmask))

        for cur_acl in cur_domain.ingress_acl_templates.get():
            print('    |- Ingress ACL: %s' % cur_acl.name)
            for cur_rule in cur_acl.ingress_acl_entry_templates.get():
                print('        |- Rule: %s' % cur_rule.description)

        for cur_acl in cur_domain.egress_acl_templates.get():
            print('    |- Egress ACL: %s' % cur_acl.name)
            for cur_rule in cur_acl.egress_acl_entry_templates.get():
                print('        |- Rule: %s' % cur_rule.description)

    print('--------------------------------------------------------------------------------')
