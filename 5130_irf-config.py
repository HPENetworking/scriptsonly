
__author__ = 'Remi Batist / AXEZ ICT Solutions'
__version__ = '1.2'
###     version 1.0: first release (support for 6 members)
###     version 1.1: adding support for 9 members
###     version 1.2: compacting script

###     Python Script for Deploying IRF-config and software on 5130 switches #########
###     WARNING!: When changing IRF Configuration, the current startup-configuration is overwritten!
###     In this script the IRF-Port-config is a fixed value for faster deploy, see settings below

###     48 Ports Switch IRF-Config
###             IRF Port  Interface                             
###             1         Ten-GigabitEthernetX/0/49            
###             2         Ten-GigabitEthernetX/0/51             
###     24 Ports Switch IRF-Config
###             IRF Port  Interface                             
###             1         Ten-GigabitEthernetX/0/25            
###             2         Ten-GigabitEthernetX/0/27

###		This script is currently supporting boot/system/PoE updates
### 	You can edit the custom config below to change the firmware/poe file-names for future releases

print "\n######## Deploying IRF-config and software on 5130 switches #########\n"

#### Custom Config

subfolder_bootfile = ""
bootfile = "5130ei-cmw710-boot-r3109p05.bin"
subfolder_sysfile = ""
sysfile = "5130ei-cmw710-system-r3109p05.bin"
subfolder_poefile = ""
poefile = "S5130EI-POE-145.bin"
tftpsrv = "192.168.0.1"

#### Importing python modules

import csv
import comware
import os
import sys
import termios

#### RAW user-input module

fd = sys.stdin.fileno();
new = termios.tcgetattr(fd)
new[3] = new[3] | termios.ICANON | termios.ECHO
new[6] [termios.VMIN] = 1
new[6] [termios.VTIME] = 0
termios.tcsetattr(fd, termios.TCSANOW, new)
termios.tcsendbreak(fd,0)

#### Get Current IRF Member
def current_id():
	current_id_i = comware.CLI('display irf link', False).get_output()
	for line in current_id_i:
		if 'Member' in line:
			s1 = line.rindex('Member') + 7
			e1 = len(line)
			current_id_r = line[s1:e1]
			return current_id_r

#### Get Available interfaces for IRF
def now_get_interface():
	result = comware.CLI('display int ten brief', False).get_output()
	for line in result:
		if '/0/28' in line:
			get_interface = 28
			return get_interface
		if '/0/52' in line:
			get_interface = 52
			return get_interface

#### User Input Software/PoE update and IRF Member-ID
def user_fud():
	sw_version = comware.CLI('display version | in Software', False).get_output()
	print '\nCurrent ' + sw_version[1]
	print '\nUpdate to latest boot/system firmware?\n'
	user_ud_r = raw_input("\ny(yes)/n(no):  ")
	return user_ud_r
def user_pud():
	comware.CLI("display poe pse | in Software")
	print '\nUpdate to latest poe-firmware?\n'
	user_ud_p = raw_input("\ny(yes)/n(no):  ")
	return user_ud_p
def user_id():
	comware.CLI('display irf link | in Member')
	print '\n#### WARNING!: When changing IRF Configuration, the current startup-configuration is overwritten! #### \n'
	print '\nSet new Member ID 1 to 9 or 0 to cancel IRF Configuration\n'
	user_id_r = raw_input("\nID:  ")
	return user_id_r

#### Deploy software
def software_u(user_ud_f, user_ud_p):
	if user_ud_f == 'y':
		print "\nUpdating software....\n"
		try:
			comware.CLI("tftp " + tftpsrv + " get " + bootfile)
			print "\nUpload successful\n"
		except SystemError as s:
			print "\nUpload successful\n"
		try:
			comware.CLI("tftp " + tftpsrv + " get " + sysfile)
			print "\nUpload successful\n"
		except SystemError as s:
			print "\nUpload successful\n"
		try:
			comware.CLI("boot-loader file boot flash:/" + bootfile + " system flash:/" + sysfile + " all main")
			print "\nConfiguring boot-loader successful\n"
		except SystemError as s:
			print "\nChange bootloader successful\n"
	if user_ud_p == 'y':
		pse_number = ["4", "7", "10", "13", "16", "19", "22", "25", "28"]
		try:
			comware.CLI("tftp " + tftpsrv + " get " + poefile)
			print "\nUpload successful\n"
		except SystemError as s:
			print "\nUpload unsuccessful\n"
		for n in pse_number:
			try:
				comware.CLI("system ; poe update full " + poefile + " pse " + n)
				print "\nPoE-Update successful\n"
			except SystemError as s:
				print "\nSkipping PoE-Update, member not available\n"


#### Deploy IRF-config
def deploy(current_id_r, user_id_r, get_interface):
	if get_interface == 52:
		print '\ndeploying 48 ports switch...\n'
	if get_interface == 28:
		print '\ndeploying 24 ports switch...\n'
	if user_id_r == '0':
		print '\nIRF Member-configuration not changed!\n'
	if user_id_r != '0':
		prio_numbers = {"1":"32","2":"31","3":"30","4":"29","5":"28","6":"27","7":"26","8":"25","9":"24"}
		prio_set = prio_numbers[user_id_r]
		comware.CLI("system ; irf member " + current_id_r + " renumber " + user_id_r)
		startup_file = open('startup.cfg', 'w')
		startup_file.write("\nirf member "+ user_id_r +" priority "+ prio_set + "\n")
		if get_interface == 52:
			startup_file.write("\nirf-port "+ user_id_r +"/1\n")
			startup_file.write("\nport group interface Ten-GigabitEthernet"+ user_id_r +"/0/49\n")
		if get_interface == 28:
			startup_file.write("\nirf-port "+ user_id_r +"/1\n")
			startup_file.write("\nport group interface Ten-GigabitEthernet"+ user_id_r +"/0/25\n")
		if get_interface == 52:
			startup_file.write("\nirf-port "+ user_id_r +"/2\n")
			startup_file.write("\nport group interface Ten-GigabitEthernet"+ user_id_r +"/0/51\n")
		if get_interface == 28:
			startup_file.write("\nirf-port "+ user_id_r +"/2\n")
			startup_file.write("\nport group interface Ten-GigabitEthernet"+ user_id_r +"/0/27\n")
		startup_file.close()
		comware.CLI("startup saved-configuration startup.cfg")
	comware.CLI("reboot force")
		
#### Define main function
def main():
	current_id_r = current_id()
	get_interface = now_get_interface()
	user_id_r = user_id()
	user_ud_f = user_fud()
	user_ud_p = user_pud()
	software_u(user_ud_f, user_ud_p)
	deploy(current_id_r, user_id_r, get_interface)
	
			
if __name__ == "__main__":
	main()

		
		
		



