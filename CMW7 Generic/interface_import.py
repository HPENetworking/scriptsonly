

__version__ = '1.3'
__author__ = 'Remi Batist'

# Version 1.0: Initial version
# Version 1.3: Allowing more the 10 VLAN's and "to" in the permitvlan column

# Importing interface-settings from pre-defined csv-file

# used row format shown in the example below
# csv delimiter ' ; '

# interface	                description	linktype		permitvlan     	pvid
# GigabitEthernet1/0/21	        server-1	access		                	23
# GigabitEthernet1/0/22	        server-2	trunk	                10 12 to 15     10


#### Importing python modules

import csv
import textwrap
import comware
import os
import sys
import termios

#### File input module

fd = sys.stdin.fileno();
new = termios.tcgetattr(fd)
new[3] = new[3] | termios.ICANON | termios.ECHO
new[6] [termios.VMIN] = 1
new[6] [termios.VTIME] = 0
termios.tcsetattr(fd, termios.TCSANOW, new)
termios.tcsendbreak(fd,0)

#### Importing file
def importFile():
	print ''
	file_in = raw_input("\nEnter filename to import:  ")
	print "\n\nStart reading file: " + file_in + ".........."
	return file_in
		
#### Open and read file
def openFile(file_in):
	try:
		fo = open (file_in)
		reader = csv.DictReader(fo, delimiter=';')
		fh = list(reader)
	except IOError as e:
		print("\nError %d reading file ' %s '\n" % (e.errno, e.filename) )
		quit()
	return fh


#### Process file, creating config lines based on csv-file.
def processFile(fh):
	try:
		numVlans = 0
		output_list = []
		item_in_1 = 'interface'
		item_in_2 = 'description'
		item_in_3 = 'linktype'
		item_in_4 = 'permitvlan'
		item_in_5 = 'pvid'
		for row in fh:
			if row[item_in_3] == 'access':
				linktype = 'port link-type access'
				set_pvid = 'port access vlan '
				set_permit =''
				output_list.append("system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + row[item_in_4]))
			else:
				linktype = 'port link-type trunk'
				set_pvid = 'port trunk pvid vlan '
				set_permit ='port trunk permit vlan '
				numVlans = len(row[item_in_4].split())
				splitVlans = ''
				if numVlans > 10:
					setVlans = (row[item_in_4].split())
					for prev,cur,next in zip([None]+setVlans[:-1], setVlans, setVlans[1:]+[None]):
						numVlans = len(splitVlans.split())
						if (numVlans == 8 and next == 'to' or numVlans == 9 and next == 'to'):
							output_list.append("system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + splitVlans))
							splitVlans = ''
						splitVlans += (cur  + " ")
						numVlans = len(splitVlans.split())
						if numVlans == 10:
							output_list.append("system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + splitVlans))
							splitVlans = ''
					output_list.append("system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + splitVlans))
				else:
					output_list.append("system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + row[item_in_4]))
		return output_list
	except KeyError as k:
		print "\nRow-name ", k, " could not be identified, please check your csv-file\n"
		sys.exit("Quiting script!\n")

#### Deploy config-lines
def deployConfig(output_list):
	failures = 0
	fail_list = []
	for i in output_list:
		print "\nDeploying Configuration....\n"
		try:
			comware.CLI(i)
			print "\nInterface configuration successful\n"
		except SystemError as s:
			try:
				failures += 1
				fail_list.append(i)
				print "\nA part of the interface configuration failed, please check your csv-file or switch-config\n"
				raw_input("Press Enter to continue or CTRL-D to abort the deployment")
			except EOFError:
				sys.exit("\nQuiting script!\n")
			except KeyboardInterrupt:
				sys.exit("\nQuiting script!\n")
	return failures, fail_list

#### Print end result
def result(failures, fail_list):
	if failures > 0:
		print "\n\nDeployment partially completed"
		print "\nItems failed: ", failures, "\n"
		for index, item in enumerate(fail_list):
			print (index + 1),":", item

	else:
		print "\n\nDeployment completed succesfuly"
		
#### Define main function
def main():
	file_in = importFile()
	fh = openFile(file_in)
	(output_list) = processFile(fh)
	(failures, fail_list) = deployConfig(output_list)
	result(failures, fail_list)
	
			
if __name__ == "__main__":
	main()

		
		
		



