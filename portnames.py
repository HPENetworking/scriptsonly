# This script is provided with no support or guarantees.
# You may use it, modify and distribute with no restrictions
# as long as original author is mentioned.
#
# Script is designed for embedded operation within Comware OS.
# It purpose is to go throw LLDP neihbors and parse remote system names.
# Then it automatically set port description in format to_remotesysname
#
# Usage:
# <Switch1>python portnames.py
# 
# You may also run script automatically when new LLDP neighbor
# is recognized by leveraging Comware EAA:
# [Switch1]rtm cli-policy LLDP_update
# [Switch1-rtm-LLDP_update]event syslog priority all msg LLDP_CREATE_NEIGHBOR occurs 1 period 1
# [Switch1-rtm-LLDP_update]action 0 cli python portnames.py
# [Switch1-rtm-LLDP_update]user-role network-admin
# [Switch1-rtm-LLDP_update]commit
#
# Author: Tomas Kubica
# Contact: tomas.kubica@hp.com



import comware

def main():
    print 'Will set port descriptions to LLDP connected devices to to_sysname'
    result = comware.CLI('display lldp neighbor-information verbose', False).get_output()
    port = ''
    name = ''
    for line in result:
        if 'LLDP neighbor-information of port' in line:
            start = line.rindex('[') + 1
            end = line.rindex(']', start)
            port = line[start:end]
        if 'System name' in line:
            start = line.rindex(':') + 2
            end = len(line)
            name = 'to_' + line[start:end]
            print 'Setting ' + port + ' description to ' + name
            comware.CLI('system-view ; interface ' + port + ' ; description ' + name +' ; return ; ', False)

if __name__ == "__main__":
    main()
