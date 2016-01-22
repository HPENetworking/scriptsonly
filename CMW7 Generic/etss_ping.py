#!/usr/bin/env python
#
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

#
#
# This script provides possibility to run range ping from the switch.
# It will access IP or range of IP addresses as parameter.
# Ranges can be specified in the following formats,
# python etss_ping.py 192.168.56.0/24 than use 192.168.56-57.0-255

__author__ = 'Dobias van Ingen'


import re
import sys

import comware


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


ip = sys.argv[1]
target_ip = etss_range(ip)
ping_opt = '-c 1'


for i in target_ip:
    cmd = comware.CLI('ping %s %s' % (ping_opt, i), False)
    output = cmd.get_output()
    a = re.search('([0-9\.]+)% packet loss', output[5])
    if float(a.group(1)) == 0.0:
        print('%s - %s' % (i, 'UP'))
    else:
        print('%s - %s' % (i, 'DOWN'))


