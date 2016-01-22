
__version__ = '0.9'
__author__ = 'Remi Batist'

# Overview of vlans including ip-addresses in procurve-style
# Example below

# VLAN-ID | IP Address       IP Subnet        NAME
# ------- | ---------------  ---------------  ---------------
#  1      |                                   VLAN 0001
#  6      |                                   VLAN 0006
#  10     | 10.10.10.2       255.255.255.0    VLAN10-SERVERS
#  20     |                                   wifi
#  30     | 10.10.30.253     255.255.255.0    VLAN30-CLIENTS


#### Importing python modules

import comware

def main():
	print 'VLAN-ID' + '\t' + '| IP Address' + '\t' + '   IP Subnet' + '\t ' + '   NAME'
	print '------- | ---------------  ---------------  ---------------'

#### Importing current information
	result = comware.CLI('display vlan all', False).get_output()
	vlanid = ''
	vlanna = ''
	vlanip = ''
	vlansn = ''
	found = False

#### Collecting specific items
	for line in result:
		if 'VLAN ID' in line:
			s1 = line.rindex(':') + 1
			e1 = len(line)
			vlanid = line[s1:e1]
			vlanip = '               '
			vlansn = '               '
		elif 'IPv4 address' in line:
			s2 = line.rindex(':') + 2
			e2 = len(line)
			vlanip = line[s2:e2]
		elif 'IPv4 subnet mask' in line:
			s5 = line.rindex(':') + 2
			e5 = len(line)
			vlansn = line[s5:e5]
		elif 'Name' in line:
			s3 = line.rindex(':') + 2
			e3 = len(line)
			vlanna = line[s3:e3]

#### Printing specific items
			print "%-7s | %-16s %-16s %s" % (vlanid, vlanip, vlansn, vlanna)

if __name__ == "__main__":
	main()
