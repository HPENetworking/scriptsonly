#!/usr/bin/env python
'''
 Copyright 2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__copyright__ = "Copyright 2016, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Flask script that auto provisions Big Switch Controller
08232016 Initial release. This script will integrate with Big Switch contoller and use the restful APIs


'''
import time
from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
# If adding a database uncomment the next two lines and adjust models.py
#from flask_sqlalchemy import SQLAlchemy
#from models import db, Switches
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import requests
requests.packages.urllib3.disable_warnings()

UPLOAD_FOLDER = APP_STATIC
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

bootstrap = Bootstrap(app)

import requests
import json
import sys

requests.packages.urllib3.disable_warnings()

controller_ip = ""
username = "admin"
password = "bsn123"
cookie = ""

def controller_request(method, path, data=""):
    if not controller_ip:
        print 'You must set controller_ip to the IP address of your BCF controller'
    controller_url = "https://%s:8443" % controller_ip
    # append path to the controller url, e.g. "https://192.168.23.98:8443" + "/api/v1/auth/login"
    url = controller_url + path
    # if a cookie exists then use it in the header, otherwise create a header without a cookie
    if cookie:
        session_cookie = 'session_cookie=%s' % cookie
        headers = {"content-type": "application/json", 'Cookie': session_cookie}
    else:
        headers = {"content-type": "application/json"}
    # submit the request
    response = requests.request(method, url, data=data, headers=headers, verify=False)
    # if content exists then return it, otherwise return the HTTP status code
    if response.content:
        return json.loads(response.content)
    else:
        return response.status_code

def authentication():
    global cookie
    method = 'POST'
    path = "/api/v1/auth/login"
    data = '{"user":"%s", "password":"%s"}' % (username, password)
    json_content = controller_request(method, path, data)
    cookie = json_content['session_cookie']

def authentication_revoke():
    method = "DELETE"
    path = '/api/v1/data/controller/core/aaa/session[auth-token="%s"]' % cookie
    status_code = controller_request(method, path)

def add_port_group(name):
    method = 'PUT'
    path = '/api/v1/data/controller/applications/bcf/port-group[name="%s"]' % name
    data = '{"name": "%s"}' % name
    controller_request(method, path, data=data)

def add_interface_to_port_group(switch, interface, port_group):
    method = 'PUT'
    path = '/api/v1/data/controller/applications/bcf/port-group  \
        [name="%s"]/member-interface[switch-name="%s"][interface-name="%s"]' % (port_group, switch, interface)
    data = '{"switch-name": "%s", "interface-name": "%s"}' % (switch, interface)
    controller_request(method, path, data=data)

def add_tenant(name):
    method = 'PUT'
    path = '/api/v1/data/controller/applications/bcf/tenant[name="%s"]' % name
    data = '{"name": "%s"}' % name
    controller_request(method, path, data=data)

def add_port_group_to_segment(port_group, segment, tenant, vlan='-1'):
    method = 'PUT'
    path = '/api/v1/data/controller/applications/bcf/tenant[name="%s"]\
        /segment[name="%s"]/port-group-membership-rule[vlan=%s][port-group="%s"]' %(tenant, segment, vlan, port_group)
    data = '{"vlan": %s, "port-group": "%s"}' %(vlan, port_group)
    controller_request(method, path, data=data)

def add_segment(name, port_groups, tenant, vlan='-1'):
    method = 'PUT'
    path = '/api/v1/data/controller/applications/bcf/tenant[name="%s"]/segment[name="%s"]' %(tenant, name)
    data = '{"name": "%s"}' % name
    controller_request(method, path, data=data)
    if port_groups:
        for port_group in port_groups:
            add_port_group_to_segment(port_group, name, tenant, vlan=vlan)

def add_port_groups(port_groups):
    """ add each port_group in list of port_groups using the function add_port_group """
    for port_group in port_groups:
        add_port_group(port_group)

def add_interfaces_to_port_group(interfaces, port_group):
    """ add each (switch, interface) pair in interfaces to port-group port_group  """
    for (switch, interface) in interfaces:
        add_interface_to_port_group(switch, interface, port_group)

if __name__ == '__main__':
    authentication()
    # Configure port-groups
    add_port_groups(['R1H1', 'R1H2', 'R2H1', 'R2H2'])
    add_interfaces_to_port_group([('R1L1', 'R1L1-eth5'), ('R1L2', 'R1L2-eth5')], 'R1H1')
    add_interfaces_to_port_group([('R1L1', 'R1L1-eth6'), ('R1L2', 'R1L2-eth6')], 'R1H2')
    add_interfaces_to_port_group([('R2L1', 'R2L1-eth5'), ('R2L2', 'R2L2-eth5')], 'R2H1')
    add_interfaces_to_port_group([('R2L1', 'R2L1-eth6'), ('R2L2', 'R2L2-eth6')], 'R2H2')
    # Configure tenants
    add_tenant('Red')
    add_segment('Web', ['R1H1'], 'Red')
    add_segment('App', ['R1H2'], 'Red')
    add_segment('DB', ['R2H1'], 'Red')
    add_tenant('Green')
    authentication_revoke()
