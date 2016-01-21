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
This is simple script to execute CLI commands from HPN switch or router via NETCONF over SSH.
This program can be easily extended to meet your own requirements. I have developed the program with
HP Network simulator. When this program is used against physical HP Comware Network switches
please change h3c.com in hp.com.
'''

__author__ = "Dobias van Ingen"
__credits__ = "Jason Edelman for insipring me in creating this program (http://www.jedelman.com/)"
__license__ = "Apache2"
__version__ = "0.3"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

from ncclient import manager
import argparse
import xml.dom.minidom


'''
This section you can provide multiple NETCONF code that will be executed
on the device
'''

display_command = """
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <CLI>
        <Execution> %s </Execution>
    </CLI>
</rpc>
"""

def exec_command(connection, command):
    # Execute command on device
    code_snip = display_command % command
    edit_response = connection.dispatch(code_snip)
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
    parser = argparse.ArgumentParser(description="Execute CLI commands via NETCONF on HP switch / router.")
    parser.add_argument("--host", help="Hostname or IP address which to connect", action="store", dest="hostname", type=str)
    parser.add_argument("--usr", help="Username of device", action="store", dest="username", type=str)
    parser.add_argument("--pass", help="Password of device", action="store", dest="password", type=str)
    parser.add_argument("--cmd", help="Command to execute on device", action="store", dest="command", type=str)

    cli_args = parser.parse_args()
    hostname = cli_args.hostname
    username = cli_args.username
    password = cli_args.password
    command = cli_args.command

    # Create connection to device
    if DEBUG: print"Set-up connection: {}\n".format(hostname)
    netconf_manager = connect_device(hostname, username, password)

    # Execute CLI command on device
    if DEBUG: print"Execute following command: {}".format(command)
    command_resp = exec_command(netconf_manager, command)
    if DEBUG: print"*** NETCONF response ***\n {}\n".format(command_resp)

    # Disconnect connection
    if DEBUG: print"Disconnect from: {}\n".format(hostname)
    disconnect_device(netconf_manager)


if __name__ == "__main__":

    main()

