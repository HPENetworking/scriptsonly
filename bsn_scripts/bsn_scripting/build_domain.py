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

Adds zones, subnets and vports to existing domain
08/20/2016 Wookieware
'''

from vspk import v3_2 as vsdk
import ipaddress

def populate_test_domain(domain, number_of_zones, number_of_subnets_per_zone, number_of_vports_per_subnet):
    """ Populate a domain with test data

        Args:
            domain (vsdk.NUDomain | vsdk.NUDomainTemplate): base domain to populate
            number_of_zones (int): number of desired zones
            number_of_subnets_per_zone (int): number of desired subnets per zone
            number_of_vports_per_subnet (int): number of desired vports per subnet (only available if domain is not a template)
    """

    # check if the domain is a template
    # if so use children template classes instead of instances
    is_template = domain.is_template()
    zone_class = vsdk.NUZoneTemplate if is_template else vsdk.NUZone
    subnet_class = vsdk.NUSubnetTemplate if is_template else vsdk.NUSubnet

    # generate a network and subnets
    network = ipaddress.ip_network(u'10.0.0.0/8')
    subnets = network.subnets(new_prefix=24)

    # create zones
    for i in range(0, number_of_zones):

        zone = zone_class(name="Zone %d" % i)
        domain.create_child(zone)
        domain.add_child(zone)

        #creates subnets
        for j in range(0, number_of_subnets_per_zone):

            # pull a subnet and get information about it
            subnetwork = subnets.next()
            ip = "%s" % subnetwork.network_address
            gw = "%s" % subnetwork.hosts().next()
            nm = "%s" % subnetwork.netmask

            subnet = subnet_class(name="Subnet %d %d" % (i, j), address=ip, netmask=nm, gateway=gw)
            zone.create_child(subnet)
            zone.add_child(subnet)

            # if the given domain is a template, we stop
            if is_template:
                break

            # Otherwise we create the VPorts
            for k in range(0, number_of_vports_per_subnet):

                vport = vsdk.NUVPort(name="VPort %d-%d-%d" % (i, j, k), type="VM", address_spoofing="INHERITED", multicast="INHERITED")
                subnet.create_child(vport)
                subnet.add_child(vport)


if __name__ == "__main__":

    # Configuring a connection to the VSD API
    nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")

    # Actively connecting ot the VSD API
    nc.start()
    print ('Auth success')

    # get a domain
    domain = nc.user.domains.get_first(filter='name == "12 Monkeys"')
    # domain = vsdk.NUDomain(name='Banner')
    print domain.id
    domain.fetch()

    # do the job
    populate_test_domain(domain, 3, 4, 5)
