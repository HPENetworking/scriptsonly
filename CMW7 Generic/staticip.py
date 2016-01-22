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

# This script is provided with no support or guarantees.
# You may use it, modify and distribute with no restrictions
# as long as original author is mentioned.
#
# Script is designed for embedded operation within Comware OS on HP 5130EI Switch.
# It purpose is to check if servers with static ip is plugged in the right port on the switch.
# If wrong port is detected, it then automatically send syslog message to inform administrator
# Administrator has to declare ip in the corresponding interface description.
# For example,
# interface GigabitEthernet1/0
#   description 192.168.0.13
#
# Usage:
# <Switch1>python staticip.py
#
# You may also run script automatically when link up/down interface
# is recognized by leveraging Comware EAA:
# [Switch1]rtm cli-policy POL1
# [Switch1-rtm-POL1]event syslog priority all msg "link status is up" occurs 1 period 1
# [Switch1-rtm-POL1]action 0 cli python staticip.py
# [Switch1-rtm-POL1]running-time 180
# [Switch1-rtm-POL1]user-role network-admin
# [Switch1-rtm-POL1]commit
#
# Author: Serge BAIKOFF
# Contact: serge.baikoff@hp.com


__author__ = 'SEBAIK'

import comware
import re
import syslog
import socket
ping_opt = '-c 2'

def get_config_port_ip():
    # Extract GigabitEthernet and IP port mapping from administrator Description
    output = comware.CLI('dis interface GigabitEthernet brief description', False).get_output()
    ip = re.compile(r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", re.VERBOSE)
    int = re.compile(r"GE[1-9]/[0-9]/[0-9]{1,2}", re.I)
    tab = []
    for i in output:
       n = ip.search(i)
       m = int.search(i)
       if n and m :
            tab.append(n.group(0))
            m = m.group(0).replace("GE", "GigabitEthernet")
            tab.append(m)
       else:
            continue
    # Convert list to dictionnairy
    result = dict(tab[i:i+2] for i in range(0, len(tab), 2))
    return result

def list_live_ip(ip):
     # Ping IP list
     for i in ip.keys():
         cmd = comware.CLI('ping %s %s' % (ping_opt, i), False)
     return 'none'

def arp(ip):
    # Return GigabitEthernet interface where ip is detected by checking arp mapping
    cmd = comware.CLI('dis arp | inc %s' % ip, False)
    output = cmd.get_output()
    if len(output) == 1:
        return 'none'
    else:
        a = re.search(ip, output[1])
        if a.group(0) == ip:
            b = output[1].split()
            c = b[3].replace("GE", "GigabitEthernet")
            return c
        else:
            return 'none'

def main():
    config = get_config_port_ip()
    list_live_ip(config)
    for i in config.keys():
        if arp(i) == config[i]:
            continue
        if arp(i) == 'none':
            syslog.openlog( 'WARNING', 0, syslog.LOG_LOCAL7 )
            syslog.syslog(syslog.LOG_ALERT, '%s %s IS NOT ACTIVE ' % (socket.gethostname(), i))
        else:
            syslog.openlog( 'WARNING', 0, syslog.LOG_LOCAL4 )
            syslog.syslog(syslog.LOG_ALERT, '%s %s IS IN WRONG PORT %s AND SHOULD BE IN %s ' % (socket.gethostname(), i, arp(i),config[i] ))

if __name__ == "__main__":
    main()
