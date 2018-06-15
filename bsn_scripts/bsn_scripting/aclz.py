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

Build a complete domain, zones, subnets and vports
08/20/2016 Wookieware
'''

from vspk import v3_2 as vsdk
import time

# Root User Login
nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")
nuage_user = nc.user

# Actively connecting ot the VSD API
nc.start()
print ('Auth success')

# Get the domain
domain = nc.user.domains.get_first(filter='name == "Conservatory"')

# Creating the job to begin the policy changes
job = vsdk.NUJob(command='BEGIN_POLICY_CHANGES')
domain.create_child(job)
# wait for the job to finish
while True:
    job.fetch()
    if job.status == 'SUCCESS':
        break
    if job.status == 'FAILED':
        print "Job failed!"
        break
    time.sleep(1)# can be done with a while loop

# Creating a new Ingress ACL
ingressacl = vsdk.NUIngressACLTemplate(
    name='Middle Ingress ACL',
    priority_type='NONE', # Possible values: TOP, NONE, BOTTOM (domain only accepts NONE)
    priority=100,
    default_allow_non_ip=False,
    default_allow_ip=False,
    allow_l2_address_spoof=False,
    active=True
    )
domain.create_child(ingressacl)

# Creating a new Ingress ACL rule to allow database connectivity
# from the Web-Tier Zone to the DB-Tier Zone
from_network = domain.zones.get_first(filter='name == "WEB Zone2"')
to_network = domain.zones.get_first(filter='name == "DB Zone2"')
db_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
    action='FORWARD',
    description='Allow MySQL DB connections from Web Zone2',
    ether_type='0x0800',
    location_type='ZONE',
    location_id=from_network.id,
    network_type='ZONE',
    network_id=to_network.id,
    protocol='6',
    source_port='*',
    destination_port='3306',
    dscp='*'
    )
ingressacl.create_child(db_ingressacl_rule)
''' Fix this code
# Creating a new Ingress ACL rule to allow Web-Net VMs to
# talk to each other on port 80
network = domain.subnets.get_first(filter='name == "Subnet 0 0"')
web_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
    action='FORWARD',
    description='Allow HTTP connections between Web-NET VMs',
    ether_type='0x0800',
    location_type='SUBNET',
    location_id=network.id,
    network_type='SUBNET',
    network_id=network.id,
    protocol='6',
    source_port='*',
    destination_port='80',
    dscp='*'
    )
ingressacl.create_child(web_ingressacl_rule)
'''
# Applying the changes to the domain
job = vsdk.NUJob(command='APPLY_POLICY_CHANGES')
domain.create_child(job)
