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
# Test server port
#
# Test / monitor if server port is open

__author__ = 'Dobias van Ingen'


import socket
import getopt
import sys


def usage():
    print "Usage: python etss_server.py -i <ip address>  -p 'Port number'"
    print "     -i --ip     Provide IP address from server to test"
    print "     -p --port   Provide port number (service) to test"
    print "     -h --help   Provide this help"
    print "Example:"
    print "     Test Telnet"
    print "         etss_server.py --ip 192.168.56.203 --port 23"
    print ""


def client_socket():
    try:
        # define IPv4 socket based on TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
            print "Failed to create socket. Error code: " + str(msg[0]) + " , Error message: " + msg[1]
            sys.exit()
    print "Socket is created"
    return s


def connect_socket(s, host_ip, port):
    try:
        s.connect((host_ip, port))
    except socket.error, msg:
        print "Unable to connect socket, Error code: %s ,\nError message: %s. Program will exit" % (str(msg[0]), msg[1])
        sys.exit()
    print "Socket connected to port %s on ip %s" % (port, host_ip)

def main():
    # need to define = for options that need input
    long_args = ["ip=", "port=", "help"]
    try:
        # need to define : for optionals that need input
        opts, args = getopt.getopt(sys.argv[1:], "i:p:h", long_args)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    host_ip = None
    port = None

    for o, a in opts:
        if o in ("-i", "--ip"):
            host_ip = a
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    s = client_socket()
    connect_socket(s, host_ip, port)
    s.close()


### Main Code
if __name__ == "__main__":
    main()
