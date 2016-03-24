#!/usr/bin/env python
#
# Copyright (c)  2013 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, fpenrlowee of charge, to any person
# obtaining a copy of this software  and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

''' This script can be run from management station or any other system in the mobile first network. A IP range
 of ArubaOS devices can be provided in combination with file and domain name. This program will retrieve hostname and
 vlan info. Based on retrieved information default hostname for each IP name will be created and dns forward and
 reverse mapping files for linux, bsd will be created. When doing traceroutes or other troubleshooting commands better
 path visibility will be seen. IP Ranges can be specified in following formats:
        - --ip 192.168.56.0-10 or for e.g. 192.168.56-57.1
'''

__author__ = "Dobias van Ingen"
__credits__ = "Kirk Byers for creating netmiko and Jason Edelman for contributing to netmiko"
__license__ = "Apache2"
__version__ = "0.1"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

from netmiko import ConnectHandler
from datetime import datetime
import argparse


def ip_range(iprange):
    hosts = []
    block = iprange.split('.')
    for x, y in enumerate(block):
        if '-' in y:
            blockrange = y.split('-')
            for z in range(int(blockrange[0]), int(blockrange[1]) + 1):
                ipaddr = '.'.join(block[:x] + [str(z)] + block[x + 1:])
                hosts += ip_range(ipaddr)
            break
    else:
        hosts.append(iprange)
    return hosts


def connect_ssh(target_ip, username, password, DEBUG, output):

    if DEBUG:
        verbose = True
    else:
        verbose = False

    dns_list = list()

    for i in target_ip:
        try:

            # Define variables for function
            x, z, v = 0, 1, 2
            vlan_list = list()
            output += ("*" * 4 + " START device: %s " + "-" * 35 + ">" * 4 + "\n") % i
            ssh_con = ConnectHandler(device_type='hp_procurve', ip=i, username=username, password=password,
                                         verbose=verbose)

            # Find hostname will be used for first part of VLAN IP dns name
            output += "\nFind prompt: \n"
            output_cmd = ssh_con.find_prompt()
            hostname = output_cmd
            if DEBUG: print hostname
            output += output_cmd

            # Get VLAN information from switch
            output_cmd = ssh_con.send_command('show vlan custom id name ipaddr')
            vlan_output = output_cmd.split(' ')
            output += output_cmd

            # Clean output information
            vlan_output = filter(None, vlan_output)

            # Filter VLAN ID's
            for y in vlan_output[18:-1]:
                if y != '\n':
                    vlan_list.append(y)
            if DEBUG: print vlan_list
            lp = len(vlan_list) / 3
            while lp != 0:
                vlan_name = hostname[:-1] + '-' + 'VL' + vlan_list[x] + '-' + vlan_list[z]
                dns_list.append(vlan_name)
                dns_list.append(vlan_list[v])
                x += 3
                z += 3
                v += 3
                lp -= 1
            if DEBUG: print dns_list
            ssh_con.disconnect()
        except:
            print "Problem connecting with ip: %s" % (i)
            continue

    return output, dns_list


def savefile(writefile, dns_list, DEBUG, domain="test"):
    try:
        if DEBUG: print "Start writing to file\n"
        if DEBUG: print domain
        f = open(writefile, "w")
        i = len(dns_list) / 2
        x, y = 0, 1
        while i != 0:
            # Verify if it needs to create forward or reverse mapping file
            if 'forward' in writefile:
                line = '{:40} {:15} {:25}\n'.format(dns_list[x], "IN A", dns_list[y])
            else:
                ip = str(dns_list[y])
                ip = ip.split('.')
                line = '{:40} {:15} {:}.{}.\n'.format(ip[3], "PTR", dns_list[x], domain)
            if DEBUG: print line
            f.writelines(line)
            x += 2
            y += 2
            i -= 1
        f.close()
    except:
        raise


def main():
    try:
        # Argument parsing
        parser = argparse.ArgumentParser(description="Collect interfaces and hostname for better DNS registration")
        parser.add_argument("-i", "--ip", help="Hostname or IP address which to connect", action="store", dest="ip", type=str)
        parser.add_argument("-u", "--usr", help="Username of device", action="store", dest="username", type=str)
        parser.add_argument("-p", "--pass", help="Password of device", action="store", dest="password", type=str)
        parser.add_argument("-d", "--domain", help="Provide domain name", action="store", dest="domain", type=str)
        parser.add_argument("-f", "--file",
                            help="Enable write to file please provide filename without extension. Default value is disabled.",
                            default='none', action="store", dest="writefile", type=str)
        parser.add_argument("-v", "--verbose", help="Enable debug mode. Default is disabled",
                            default=False, action="store_true", dest="debug")

        # Parse all arguments in variables
        cli_args = parser.parse_args()
        ip = cli_args.ip
        username = cli_args.username
        password = cli_args.password
        domain = cli_args.domain
        writefile = cli_args.writefile
        deb = cli_args.debug

        # Set DEBUG value
        DEBUG = deb

        # Call function IP Range to split ip addresses in list
        target_ip = ip_range(ip)

        # Print session information
        if DEBUG: print """ SSH connection will be set-up with following parameters:
        IP Range        : %s
        Username        : %s
        Password        : %s
        Domain          : %s
        Write to file   : %s
        Debug           : %s
        """ % (target_ip, username, password, domain, writefile, deb)

        # Start timing run time
        start_time = datetime.now()
        if DEBUG: print "Start time: %s" % (start_time)

        output = "ArubaOS Mobile Infrastructure DNS configuration:\n"

        # Start connecting to devices
        outputtotal, dns_list = connect_ssh(target_ip, username, password, DEBUG, output)

        # End time and calculate total run time
        end_time = datetime.now()
        total_time = end_time - start_time

        if DEBUG: print "End time: %s" % (end_time)
        if DEBUG: print "Total run time: %s" % (total_time)

        outputtotal += "\nArubaOS Mobile Infrastructure run time summary:\n"
        outputtotal += "Command output(s)started on: %s\n" % (start_time)
        outputtotal += "Command output(s)ended on: %s\n" % (end_time)
        outputtotal += "Command output(s)total run time: %s\n" % (total_time)
        if DEBUG: print outputtotal
        if DEBUG: print dns_list

        # Write output for forwarding mapping zone to file when file name is provided
        writefilefwd = writefile + '_forward.txt'
        if writefile != "none": savefile(writefilefwd, dns_list, DEBUG)

        # Write output for reverse mapping zone to file when file name is provided
        writefilerevs = writefile + '_reverse.txt'
        if DEBUG: print domain
        if writefile != "none": savefile(writefilerevs, dns_list, DEBUG, domain)

        if DEBUG: print "Closing ArubaOS Mobile Infrastructure application ...\n"
    except SystemExit:
        print "There is an error in arguments provided!"
    except:
        print "Error in program and to lazy to configure better error handling 8-)"
        raise


if __name__ == "__main__":
    main()
