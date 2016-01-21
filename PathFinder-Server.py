#******************************************************************************
# MAC path finder - Server part
#		equivalent to traceroute but based on MAC address
# Version: 1.0
# Revision history: 
# 		1.0 - 30/06/2014 : Initial coding (Yannick Castano, Hewlett-Packard)
#
# Pre-requisite: LLDP enables on all switch to switch interfaces
#				 Management IP address configured on the lowest VLAN interface
#
# Remarks:		 This script needs more testing
#				 You can launch server script through scheduler job command
#				 Any comment/feedback is welcome: castano@hp.com
#******************************************************************************

''' Copyright 2016 Hewlett Packard Enterprise Development LP.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''

import socket
import os
import re
import sys
import comware

__author__ = 'Yannick Castano'

#******************************************************************************
# Global variables
#******************************************************************************

SERVERPORT = 50000
CLIENTPORT = 50001

#******************************************************************************
# Procedures
#******************************************************************************

def get_lldp_mgt_ip():
	command = comware.CLI('display lldp local-information', False)
	output = command.get_output()
	local_ip = 'none'
	#Extracts the LLDP local IP management address
	for s in output:
		if s.find('Management address') != -1:
			# keeps only the line with the management IP address
			if '.' in s.split()[3]:
				local_ip = s.split()[3]
				break # stops at the first management IP address
	return local_ip
	
def find_local_mac_next_if(mac):
	command = comware.CLI('display mac-address ' + mac, False)
	output = command.get_output()
	if len(output) <= 2:
		# no mac address corresponding, result is empty
		return 'none'
	else:
		# get the third line and extract the local interface
		# first line is the command, second line the header
		result = output[2].split()
		return result [3]

def find_local_arp_ip(mac):
	command = comware.CLI('display arp | include ' + mac, False)
	output = command.get_output()
	if len(output) == 1:
		# no mac address corresponding, result is empty
		return 'none'
	else:
		# get the first line and extract the IP address
		result = output[1].split()
		return result [0]

def find_lldp_neighbor(interface):
	# LLDP rule: the lowest interface ID with an IP address is used as management interface (loopback are excluded)
	command = comware.CLI('display lldp neighbor-information interface ' + interface + ' verbose', False)
	output = command.get_output()
	neighbor = ['none', 'none']
	if len(output) != 1:
		# extracts the LLDP peer name
		for s in output:
			if s.find('System name') != -1:
				neighbor[0] = s.split()[3]
		# extracts the LLDP peer IP management address
		for s in output:
			if s.find('Management address') != -1:
				# keeps only the line with the management IP address
				if '.' in s.split()[3]:
					neighbor[1] = s.split()[3]
	return neighbor

def send_tracemac_request(originhost,neighbor_ip,mac):
	# sending on UDP port 50000
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((neighbor_ip, SERVERPORT))
	sock.sendall(originhost + ' ' + mac)
	sock.close()
	return
	
def send_tracemac_response(remotehost,message):
	# sending on UDP port 50001
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((remotehost, CLIENTPORT))
	sock.sendall(message)
	sock.close()
	return

def convert_interface_name(intf):
	# currently supports 1G, 10G and 40G interfaces
	if intf.find('XGE') != -1:
		interface = intf.replace('XGE','Ten-GigabitEthernet')
	elif intf.find('FGE') != -1:
		interface = intf.replace ('FGE', 'FortyGigE')
	elif intf.find('GE') != -1:
		interface = intf.replace ('GE', 'GigabitEthernet')
	return interface

#******************************************************************************
# Main code
#******************************************************************************
localhost = get_lldp_mgt_ip()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((localhost, SERVERPORT))
print 'Listening on ' + localhost
while True:
	received_data = sock.recv(1024)
	command_data = received_data.split()
	remotehost = command_data[0]
	mac = command_data[1]
	print 'Sender is: ', remotehost
	print 'Mac to find is: ', mac
	# Try to find if this MAC has a local ARP entry
	ip = find_local_arp_ip(mac.lower())
	if ip != 'none': 
		send_tracemac_response (remotehost,'[' + localhost + ']:\t MAC address {} has IP address {}'.format(mac,ip))
	
	# Find the interface where this MAC has been learned
	intf = find_local_mac_next_if(mac.lower())
	if intf == 'none':
		send_tracemac_response (remotehost,'[' + localhost + ']:\t No corresponding MAC address on this device')
	else:
		interface = convert_interface_name(intf)
		neighbor = find_lldp_neighbor(interface)
		if neighbor[0] == 'none':
			send_tracemac_response (remotehost,'[' + localhost + ']:\t MAC address {} is on {}'.format(mac,interface))
			send_tracemac_response (remotehost,'END')
		else:
			send_tracemac_response (remotehost,'[' + localhost + ']:\t MAC address {} is on {} via switch {} (IP: {})'.format(mac,interface,neighbor[0],neighbor[1]))
			#sending request to the next switch
			send_tracemac_request(remotehost,neighbor[1],mac)
