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

'''

 This script is used for educational purposes. It provides an overview of make POST calls towards Airwave API.

'''

__author__ = "Dobias van Ingen"
__license__ = "Apache2"
__version__ = "0.1"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

import requests
import argparse


def amp_login(username, password, DEBUG):
    data_login = 'credential_0='+username+'&credential_1='+password+'&destination=/&login=Log In'
    if DEBUG: print data_login
    header_login={'Content-Type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
    if DEBUG: print header_login

    amp_session = requests.Session()
    amp_login_session = amp_session.post('https://172.16.0.3/LOGIN', headers=header_login, data=data_login, verify=False)

    return amp_session, amp_login_session


def amp_change_template(xbiscotti, amp_session, api, DEBUG):
    header_post = {'X-BISCOTTI': xbiscotti}
    if DEBUG: print header_post
    data_post = '''<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
    <amp_template_variable_update version="1" xmlns:template_variable_api="http://www.airwave.com">
    <ap id="31">
    <custom_variable_9>'''+api+'''</custom_variable_9>
    </ap>
    </amp_template_variable_update>
    '''
    if DEBUG: print data_post

    amp_output = amp_session.post('https://172.16.0.3/template_variable_api', headers=header_post, data=data_post, verify=False)

    return amp_output


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Example of how to change template variable via Airwave API")
    parser.add_argument("-a", "--api", help="Provide value of custom ap include 9 variable value", action="store", dest="api", type=str)
    parser.add_argument("-u", "--usr", help="Username of Airwave API", action="store", dest="username", type=str)
    parser.add_argument("-p", "--pass", help="Password of Airwave API", action="store", dest="password", type=str)
    parser.add_argument("-d", "--debug", help="Enable debug mode. Default is disabled",
                            default=False, action="store_true", dest="debug")

    # Parse all arguments in variables
    API_args = parser.parse_args()
    api = API_args.api
    username = API_args.username
    password = API_args.password
    deb = API_args.debug

    # Set DEBUG value
    DEBUG = deb

        # Print session information
    if DEBUG: print """ Airwave API Template API connection:
        AP Include      : %s
        Username        : %s
        Password        : %s
        Debug           : %s
        """ % (api, username, password, deb)


    amp_session, amp_login_session = amp_login(username, password, DEBUG)
    xbiscotti = amp_login_session.headers.get('X-BISCOTTI')
    if DEBUG: print xbiscotti

    amp_output = amp_change_template(xbiscotti, amp_session, api, DEBUG)

    if DEBUG:  print amp_output
    if DEBUG:  print amp_output._content


if __name__ == "__main__":
    main()




