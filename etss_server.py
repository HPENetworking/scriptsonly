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
# Test server port
#
# Test / monitor if server port is open

__author__ = 'Dobias van Ingen'


import socket
import getopt
import sys


#message = "GET / HTTP /1.1\r\n\r\n"

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

#def send_info(message):
#    try:
#        s.sendall(message)
#    except socket.error:
#        print "Send failed"
#        sys.exit()
#    print "Send message completed"

#def recv_info():
#    reply = s.recv(4096)
#    print reply


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
