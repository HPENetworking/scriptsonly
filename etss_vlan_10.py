#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
# Configure Comware device to enable ssh with local user
# Start script username and password as arguments
#

__author__ = 'Dobias van Ingen'


import comware
import getopt
import sys

def main(argv):
    vlan_start = 0
    vlan_range = 0
    vlan_ip = ''
    try:
        opts, args = getopt.getopt(argv,"hs:r:i:",["start=","range=", "ip=", "help"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-s", "--start"):
            vlan_start = int(arg)
        elif opt in ("-r", "--range"):
            vlan_range = int(arg)
        elif opt in ("-i", "--ip"):
            vlan_ip = arg
        else:
            usage()
    if vlan_start == 0 or vlan_range == 0 or vlan_ip == '':
        usage()
    configure_vlans(vlan_start, vlan_range, vlan_ip)
    save_config()

def usage():
	print "Usage: etss_vlan.py -s <Start VLAN> -r <VLAN Range> -i <IP Address Range>"
	print "	 -h --help     Print this help"
	print "	 -s --start    VLAN ID to start vlan configuration"
	print "	 -r --range    Amount of VLANs to be configured for e.g. 3"
	print "	 -i --ip       IP address range to configure on VLAN interfaces\n" \
          "                for e.g. 192.168.200-204.1 will configure all interfaces\n" \
          "                with .1 in different subnets (default /24)"
	print ""
	print "Example:"
	print "	 Configure VLANs 200 to 203 with .254 as interface address"
	print "		 python etss_vlan.py -s 200 -r 3 -i 192.168.200-203.254"
	sys.exit(2)

def configure_vlans(vlan_start, vlan_range, vlan_ip):
	try:
		print "Configuring VLANs %s to %s" % (vlan_start, (vlan_start+vlan_range))
		config = [
				"system-view",
				"vlan %s to %s" % (vlan_start, (vlan_start+vlan_range))
				 ]
		target_ip = etss_range(vlan_ip)
		total_vlan = []
		total_vlan.append(vlan_start)

		while vlan_range != 0:
			x = vlan_start + vlan_range
			total_vlan.append(x)
			vlan_range = vlan_range - 1
		total_vlan.sort()

		for (y, z) in zip(total_vlan, target_ip):
			print "Configuring VLAN interface %s with ip %s" % (y, z)
			config.append("interface Vlan-interface %s" % y)
			config.append("  ip address %s 24" % z)
		comware.CLI(' ;'.join(config), False)

	except SystemError:
		print "Problem with syntax configuration ..."
		print "Exit program ..."
		sys.exit(1)

def etss_range(etssrange):
	hosts = []
	block = etssrange.split('.')
	for x, y in enumerate(block):
		if '-' in y:
			blockrange = y.split('-')
			for z in range(int(blockrange[0]), int(blockrange[1])+1):
				ipaddr = '.'.join(block[:x] + [str(z)] + block[x+1:])
				hosts += etss_range(ipaddr)
			break
	else:
		hosts.append(etssrange)
	return hosts

def save_config():
    print "!! Please remember to save the configuration !!"

if __name__ == "__main__":
	main(sys.argv[1:])
