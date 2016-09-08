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

# Root User
nuage_user = nc.user
domx = 'rod'
dom = nuage_user.domains.get_first(filter="name == '%s'" % domx)
dom.fetch()



#print ( dir(dom) )
#print json.dumps(dom, indent=4, sort_keys=True)
for cur_acl in dom.ingress_acl_templates.get():
    print type(cur_acl)
    print('    |- Ingress ACL: %s' % cur_acl.name)
    for cur_rule in cur_acl.ingress_acl_entry_templates.get():
        #print('        |- Rule: %s' % cur_rule.description)
        #rint cur_rule.__dict__
        print 'a ingress template rule'
        print cur_rule.action
        print cur_rule.description
        print cur_rule.protocol
        print cur_rule.dscp
        print cur_rule.destination_port
        print cur_rule.source_port
        print cur_rule.ether_type
        print cur_rule.network_id
        print cur_rule.network_type
        print cur_rule.location_type
        print cur_rule.location_id
        print '========================================'

for cur_acl in dom.egress_acl_templates.get():
    print('    |- Egress ACL: %s' % cur_acl.name)
    for cur_rule in cur_acl.egress_acl_entry_templates.get():
        print 'a egress template rule'
        print cur_rule.action
        print cur_rule.description
        print cur_rule.protocol
        print cur_rule.dscp
        print cur_rule.destination_port
        print cur_rule.source_port
        print cur_rule.ether_type
        print cur_rule.network_id
        print cur_rule.network_type
        print cur_rule.location_type
        print cur_rule.location_id
        print '========================================'

for cur_acl in dom.ingress_acl_templates.get():
        print 'a middle ingress acl'
        print cur_acl.name
        print cur_acl.priority_type
        print cur_acl.priority
        print cur_acl.default_allow_ip
        print cur_acl.default_allow_non_ip
        print cur_acl.allow_l2_address_spoof
        print cur_acl.active
        print '========================================'

for cur_acl in dom.egress_acl_templates.get():
        print 'a middle egress acl'
        print cur_acl.name
        print cur_acl.priority
        print cur_acl.description
        print cur_acl.policy_state
        print cur_acl.default_allow_ip
        print cur_acl.default_allow_non_ip
        print cur_acl.default_install_acl_implicit_rules
        print '========================================'



'''
# Creating the job to begin the policy changes
job = vsdk.NUJob(command='BEGIN_POLICY_CHANGES')
dom.create_child(job)
# wait for the job to finish
while True:
    job.fetch()
    if job.status == 'SUCCESS':
        break
    if job.status == 'FAILED':
        return render_template('fail_acls.html', domain = domain)
        break
    time.sleep(1)# can be done with a while loop
# Creating a new Ingress ACL rule to allow database connectivity
# from the Web-Tier Zone to the DB-Tier Zone
to_network = dom.zones.get_first(filter='name == "WEB Zone2"')
from_network = dom.zones.get_first(filter='name == "DB Zone2"')
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
# Applying the changes to the domain
job = vsdk.NUJob(command='APPLY_POLICY_CHANGES')
dom.create_child(job)
break

if import_job.status == 'FAILED':
print "fail"
break
time.sleep(1)
print "complete"
'''
