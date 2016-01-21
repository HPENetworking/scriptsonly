#!/usr/bin/env python

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


'''
This script collects SNMP parameters from Aruba Networks Provision switches to determine downtime of a port.
When script is executed you can provide following parameters:
-c for SNMP COMMUNITY name (v3 is not included yet)
-p for SNMP port default will be 161
-i for ip range for e.g. 192.168.56-57.1 will generate IP's 192.168.56.1, 192.168.57.1

Thanks to Kirk Byers for simplfy snmp within Python with snmp_helper module
https://github.com/ktbyers/pynet/blob/master/snmp/snmp_helper.py
'''

__author__ = "Dobias van Ingen"
__license__ = "Apache2"
__version__ = "0.2"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

from snmp_helper import snmp_get_oid, snmp_extract
from datetime import timedelta
import argparse
import textwrap


def collect_snmp(community, port, hosts, verbose):
    DEBUG= False
    # Set all SNMP OID to collect
    OID_name = '1.3.6.1.2.1.1.5.0'
    OID_descr = '1.3.6.1.2.1.1.1.0'
    SYS_uptime = '1.3.6.1.2.1.1.3.0'
    IF_oper = '1.3.6.1.2.1.2.2.1.8.'
    IF_type = '1.3.6.1.2.1.2.2.1.3.'
    IF_last = '1.3.6.1.2.1.2.2.1.9.'
    IF_desc = '1.3.6.1.2.1.2.2.1.2.'

    for y in hosts:
        try:
            test = 0
            x = 1
            lastlist = []
            intlist = []
            sw = (y, community, port)
            if DEBUG: print "DEBUG: Connecting to switch with following parameters: {}\n".format(sw)
            snmp_data = snmp_get_oid(sw, oid=OID_name)
            print "*" * 80
            print "Switch name: %s" % snmp_extract(snmp_data)
            snmp_data = snmp_get_oid(sw, oid=OID_descr)
            print "Switch description: %s" % "\n".join(textwrap.wrap(snmp_extract(snmp_data),65))
            snmp_data = snmp_get_oid(sw, oid=SYS_uptime)
            ticks = snmp_extract(snmp_data)
            seconds = float(ticks)/100
            sysup = timedelta(seconds=seconds)
            print "Systemuptime: %s" % sysup
            print "*" * 80 + "\n"
            while test == 0:
                snmp_data = snmp_get_oid(sw, oid=IF_type+str(x))
                type = snmp_extract(snmp_data)
                if 'No Such Instance' in type:
                    test = 1
                else:
                    oper = snmp_get_oid(sw,oid=IF_oper+str(x))
                    oper = snmp_extract(oper)
                    if int(oper) == 2:
                        last = snmp_get_oid(sw, oid=IF_last+str(x))
                        lastlist.append(snmp_extract(last))
                        descr = snmp_get_oid(sw, oid=IF_desc+str(x))
                        intlist.append(snmp_extract(descr))
                x = x+1
            y = 0
            for x in lastlist:
                down = float(ticks) - float(x)
                seconds = float(down)/100
                sysup1 = timedelta(seconds=seconds)
                print "Interface %s id down for: %s" % (intlist[y], sysup1)
                y = y + 1
        except:
            if verbose == "y":
                print "Error occurred when connecting to switch: %s" % str(sw)
            pass

def set_range(ip_range):
    hosts = []
    block = ip_range.split('.')
    for x, y in enumerate(block):
        if '-' in y:
            blockrange = y.split('-')
            for z in range(int(blockrange[0]), int(blockrange[1]) + 1):
                ipaddr = '.'.join(block[:x] + [str(z)] + block[x + 1:])
                hosts += set_range(ipaddr)
            break
    else:
        hosts.append(ip_range)
    return hosts

def main():
    DEBUG = False
    # Parse all arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--community", default="public", help="Provide SNMP community string, default is public (v3 not supported yet)")
    parser.add_argument("-p", "--port", default=161, help="Provide SNMP port number. Default value used will be 161")
    parser.add_argument("-i", "--ip", help="Provide ip address / range")
    parser.add_argument("-v", "--verbose", default='y', help="Enable (y) or disable (n) verbose mode")
    args = parser.parse_args()
    community = str(args.community)
    port = str(args.port)
    ip_range = str(args.ip)
    verbose = str(args.verbose)

    # Display parameters
    if verbose == 'y':
        print "\n" + "#" * 80
        print "# Parameters used to collect port downtime:".ljust(78), "#"
        print "# SNMP community name: {}".format(community).ljust(78), "#"
        print "# SNMP port number:{}".format(port).ljust(78), "#"
        print "# IP-Range:{}".format(ip_range).ljust(78), "#"

    # Call set_range function to spit ip ranges in ip addresses lists
    if DEBUG: print"# DEBUG: Split following ip range: {}".format(ip_range).ljust(78), "#"
    hosts = set_range(ip_range)
    if verbose == 'y':
        print "# Total ip addresses that will be scanned for ports downtime are: {}".format(len(hosts)).ljust(78), "#"
        print "#" * 80 + "\n"
    # Call SNMP function to collect all parameters
    collect_snmp(community, port, hosts, verbose)

if __name__ == "__main__":
    main()


