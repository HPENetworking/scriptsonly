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

dom = 'dc1'
fromzone = 'American-AirlinesZone 0'
tozone = 'American-AirlinesZone 2'
direction = 'Egress'
action = 'FORWARD'
description  = 'Allow me'
ethertype= '0x0800'
protocol= '6'
sourceport = '*'
destinationport = '5050'
dscp = '*'

domain = nuage_user.domains.get_first(filter="name == '%s'" % dom)
domain.fetch()

from_network = domain.zones.get_first(filter="name == '%s'" % fromzone)
#print from_network.id
to_network = domain.zones.get_first(filter="name == '%s'" % tozone)
#print to_network.id

if direction == 'Ingress':
    for in_acl in domain.ingress_acl_templates.get():
        db_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
            action=action,
            description=description,
            ether_type=ethertype,
            location_type='ZONE',
            location_id=from_network.id,
            network_type='ZONE',
            network_id=to_network.id,
            protocol=protocol,
            source_port=sourceport,
            destination_port=destinationport,
            dscp=dscp
            )
        in_acl.create_child(db_ingressacl_rule)

if direction == 'Egress':
    for out_acl in domain.egress_acl_templates.get():
        db_egressacl_rule = vsdk.NUEgressACLEntryTemplate(
            action=action,
            description=description,
            ether_type=ethertype,
            location_type='ZONE',
            location_id=from_network.id,
            network_type='ZONE',
            network_id=to_network.id,
            protocol=protocol,
            source_port=sourceport,
            destination_port=destinationport,
            dscp=dscp
            )
        out_acl.create_child(db_egressacl_rule)
print 'finsush'
