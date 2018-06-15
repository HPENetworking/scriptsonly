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
'''
#print vsdk.NUSubnet().children_rest_names
# Output:
# ['statistics', 'qos', 'eventlog', 'addressrange', 'dhcpoption', 'vm', 'virtualip', 'ipreservation', 'vminterface', 'resync', 'tca', 'vport', 'statisticspolicy', 'metadata']

# Get enterprisess
print ('Printing Enterprises')
enterprises = nuage_user.enterprises.get()

for ent in enterprises:
    print ('Printing the enterprise name %s') % (ent.name)
    print ('Printing the enterprise id %s') % (ent.id)
# Sample output:
# Finance Department
# HR Department
#enterprise = vsdk.NUEnterprise(name='New Test Enterprise')
#print enterprise
# Output:
# None
# nuage_user.create_child(enterprise)
#print ('This is the ID of the newly created enterprise %s') % (enterprise.id)
# Output:
# 1f5547c7-3ed5-4aec-a135-a17fcdb35438
zone = vsdk.NUZone(name='Test5')
domain = vsdk.NUDomainTemplate(name='Zerk')
enterprise = vsdk.NUEnterprise(name="Enterprise ElvisB")
print ('Printing the domain id %s') % (domain.id)
print domain.name
print ('Look above me')
domain = nuage_user.domains.get_first(filter='name == "Default Domain"')
domain.fetch()


job = vsdk.NUJob(command='EXPORT')

# Creating export job for the Main VSPK Domain

domain.create_child(job)

# Printing the export result

while True:
    job.fetch()
    if job.status == 'SUCCESS':
        print json.dumps(job.result, indent=4, sort_keys=True)
        #print job.result['parameters']['domain'][0:1][0]['name']
        print job.result['parameters']['domain'][0]['modifyableAttributes']['name']['value']
        print type(job.result)
        break

    if job.status == 'FAILED':
        break
    time.sleep(1)
'''
x = vsdk.NUIngressACLTemplate().children_rest_names
y = vsdk.NUEgressACLTemplate().metadata
print "ingress"
print json.dumps(x, indent=4, sort_keys=True)
print "Egress"
print json.dumps(y, indent=4, sort_keys=True)
#acl = nuage_user.ingressacls.get_first()
print "metadata"
print y[2]
# users = nuage_user.users.get_first()
# print users
#x = ( dir(user) )
#x = ( dir(acl) )

print type(y[2])
print json.dumps(x, indent=4, sort_keys=True)
#print x[69]
#print x[91]
#print x[110]
#print x[121]
