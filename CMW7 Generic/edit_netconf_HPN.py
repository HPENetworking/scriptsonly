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
This programs provides network automation via NETCONF over SSH with HP Networking switch devices.
Multiple configuration examples can be automated. This program can be easily extended to meet
your own requirements. I have developed the program with HP Network simulator. When this program is used against
physical HP Comware Network switches please change h3c.com in hp.com.

Usage:
<script name> -h for help message
             --host <HOSTNAME> for hostname or IP which to make NETCONF connection
             --usr <USERNAME> username of device to set-up NETCONF connection
             --pass <PASSWORD> password of device to set-up NETCONF connection
             --name <SYSNAME> this is system name that device will get
'''

__author__ = "Dobias van Ingen"
__credits__ = "Jason Edelman for insipring me in creating this program (http://www.jedelman.com/)"
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

import argparse
from ncclient import manager

'''
This section you can provide multiple NETCONF code that will be executed
on the device
'''

change_sysname = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <Device>
            <Base>
                <HostName> %s </HostName>
            </Base>
        </Device>
    </top>
</config>
"""

add_vlan = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <VLAN>
            <VLANs>
                <VLANID>
                    <ID> %s </ID>
                </VLANID>
            </VLANs>
        </VLAN>
    </top>
</config>
"""

def c_hostname(connection, systemname):
    # Change system name of device
    code_snip = change_sysname % systemname
    edit_response = connection.edit_config(target='running', config=code_snip, default_operation="replace")
    return edit_response

def a_vlan(connection, vlan_id):
    # Add VLAN to device
    code_snip = add_vlan % vlan_id
    edit_response = connection.edit_config(target='running', config=code_snip, default_operation="replace")
    return edit_response


def connect_device(hostname, username, password):
    # Set-up NETCONF over SSH session
    netconf_manager = manager.connect(host=hostname,
                                    port=830,
                                    username=username,
                                    password=password,
                                    hostkey_verify=False,
                                    allow_agent=False,
                                    look_for_keys=False
                                  )
    return netconf_manager

def disconnect_device(connection):
    # Close NETCONF session and transport
    connection.close_session()

def main():
    DEBUG = True

    # Argument parsing
    parser = argparse.ArgumentParser(description="Automate multiple HP switch / router configuration settings")
    parser.add_argument("--host", help="Hostname or IP address which to connect", action="store", dest="hostname", type=str)
    parser.add_argument("--usr", help="Username of device", action="store", dest="username", type=str)
    parser.add_argument("--pass", help="Password of device", action="store", dest="password", type=str)
    parser.add_argument("--name", help="System name to change on device", action="store", dest="sysname", type=str)
    parser.add_argument("--vlid", help="VLAN ID to add to device", action="store", dest="vlanid", type=str)

    cli_args = parser.parse_args()
    hostname = cli_args.hostname
    username = cli_args.username
    password = cli_args.password
    sysname = cli_args.sysname
    vlan_id = cli_args.vlanid

    # Create connection to device
    if DEBUG: print"Set-up connection: {}\n".format(hostname)
    netconf_manager = connect_device(hostname, username, password)

    # Change systemname on device
    if DEBUG: print"Change systemname to: {}".format(sysname)
    sysname_resp = c_hostname(netconf_manager, sysname)
    if DEBUG: print"*** NETCONF response ***\n {}\n".format(sysname_resp)

    # Add VLAN on device
    if DEBUG: print"Add VLAN id: {}".format(vlan_id)
    addvlan_resp = a_vlan(netconf_manager, vlan_id)
    if DEBUG: print"*** NETCONF response ***\n {}\n".format(addvlan_resp)


    # Disconnect connection
    if DEBUG: print"Disconnect from: {}\n".format(hostname)
    disconnect_device(netconf_manager)


if __name__ == "__main__":

    main()

