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
# Configure Comware device to enable ssh with local user
# Start script username and password as arguments

__author__ = 'Dobias van Ingen'

import sys
import comware

def configure_ssh(user, password):
    print "Configuring SSH and local user"
    config = [
                "system-view",
                "public-key local create rsa",
                "ssh server enable",
                "local-user {} class manage".format(user),
                "password simple {}".format(password),
                "authorization-attribute user-role network-admin",
                "service-type ssh",
                "line vty 0 63",
                "authentication-mode scheme",
                "protocol inbound ssh"
            ]
            ]

    configure_switch(config)
    save_config()

def configure_switch(config):

    try:
        comware.CLI(' ;'.join(config), False)
    except SystemError:
        print "Problem with syntax configuration ..."
        print "Exit program ..."
        sys.exit(1)

def save_config():

    try:
        comware.CLI("save ssh_config.cfg", False)
    except:
        print "The configuration file couldn't be saved ..."
        print "Program will exit ..."
        sys.exit(1)


# Main code

if len(sys.argv) <= 1:
    print "No arguments provided. Please start script with SSH user and password as arguments."
else:
    user = str(sys.argv[1])
    password = str(sys.argv[2])
    configure_ssh(user, password)


