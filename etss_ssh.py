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


