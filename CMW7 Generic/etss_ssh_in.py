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

import paramiko
import sys
import os
import time

test = os.system('ping 192.168.56.102')

cmd = "display version\n"
host = '192.168.56.102'
user = 'dobias'
passwd = 'HPRocks2'

ip = sys.argv[1]


def screen_disable(remote):
    #Turn of pausing between screens of output

    remote.send('screen-length disable\n')
    time.sleep(1)

    #Clear the on screen buffer
    output = remote.recv(1000)

    return output

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



def main():
    target_ip = etss_range(ip)
    print target_ip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in target_ip:
        try:
            ssh.connect(i, username=user, password=passwd)
            print "SSH connection established to %s" % (i)
            remote = ssh.invoke_shell()
            print "Interactive SSH session established"
            output = remote.recv(1000)
            print output
            #Disable pausing between screens of output
            screen_disable(remote)
            #Send commands to network device
            remote.send('\n')
            remote.send(cmd)
            time.sleep(2)
            output = remote.recv(5000)
            print output
        except:
            ssh.close()
            print "Problem connecting with ip: %s" % (i)
            continue

if __name__ == "__main__":
    main()

