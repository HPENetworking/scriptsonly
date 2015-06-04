

__version__ = '0.9'
__author__ = 'Remi Batist'

# Importing interface-settings from pre-defined csv-file

# used row format shown in the example below
# csv delimiter ' ; '

# interface	                	  description	  linktype		  permitvlan     	pvid
# GigabitEthernet1/0/21	        server-1	    access		                	  23
# GigabitEthernet1/0/22	        server-2	    trunk	        10 12	          10


#### Importing python modules

import csv
import comware
import os
import sys
import termios

#### File input function

fd = sys.stdin.fileno();
new = termios.tcgetattr(fd)
new[3] = new[3] | termios.ICANON | termios.ECHO
new[6] [termios.VMIN] = 1
new[6] [termios.VTIME] = 0
termios.tcsetattr(fd, termios.TCSANOW, new)
termios.tcsendbreak(fd,0)

print ''
file_in = raw_input(" csv-file to import: ")


#### Importing rows
item_in_1 = 'interface'
item_in_2 = 'description'
item_in_3 = 'linktype'
item_in_4 = 'permitvlan'
item_in_5 = 'pvid'


#### Open file

with open(file_in,'r') as f:
	reader = csv.DictReader(f, delimiter=';')
	rows = list(reader)

#### Reading file
for row in rows:

#### Setting link-type

	if row[item_in_3] == 'access':
		linktype = 'port link-type access'
		set_pvid = 'port access vlan '
		set_permit =''
	else:
		linktype = 'port link-type trunk'
		set_pvid = 'port trunk pvid vlan '
		set_permit ='port trunk permit vlan '
	
#### Deploying settings

	print ''
	print 'Deploying settings...'
	print ''
	strcli = "system ;%s ;%s ;%s ;%s ;%s" % ('interface '+row[item_in_1], 'description ' +row[item_in_2], linktype, set_pvid + row[item_in_5], set_permit + row[item_in_4])
	comware.CLI(strcli)


		
		
		



