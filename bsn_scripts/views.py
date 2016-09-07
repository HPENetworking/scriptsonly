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

# Routes
@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        global session_cookie
        global cookie
        global controller_url
        user = request.form.get('user')
        password = request.form.get('passwd')
        host= request.form.get('host')
        controller_url = 'https://' + host + ':8443'

        # Actively connecting ot the VSD API
        try:
            ##################################
            # Login
            ##################################
            # First you must obtain an authentication cookie from the controller, we therefore define the login path
            path = "/api/v1/auth/login"
            # append the login path to the controller url to obtain the full url
            url = controller_url + path

            # Define the data and headers for the HTTP request
            data = '{"user": "' + user +'", "password": "' + password + '"}'
            headers = {"content-type": "application/json"}

            # POST request made on the Big Cloud Fabric controller
            response = requests.request('POST', url, data=data, headers=headers, verify=False)

            # Extract the cookie from the response and create a session cookie string to be used in subsequent requests
            cookie = json.loads(response.content)['session_cookie']
            session_cookie = 'session_cookie=%s' % cookie

        except:
            flash('Login Session Failed...Check Credentials')
            return render_template('main.html', error = error)
        return render_template('menu.html', error = error)
    return render_template('main.html', error = error)

# Select record for editing
@app.route('/return_to', methods = ['GET', 'POST'])
def return_to():
    return render_template('menu.html')

# Select record for editing
@app.route('/show_switch', methods = ['GET'])
def show_switch():
    error = None
    count = 0
    switches = []
    switch = []
    try:
        # path is set to substring "/api/v1/data/controller/applications/bcf/info/fabric/switch" from the above url
        path = '/api/v1/data/controller/applications/bcf/info/fabric/switch'
        # we append this "show switch" path to the controller url to obtain a full url
        url = controller_url + path

        # There is no data to pass in for this GET request
        data = ''
        # the headers will contain the session cookie we obtained above via the POST request
        headers = {"content-type": "application/json", 'Cookie': session_cookie}

        response = requests.request('GET', url, data=data, headers=headers, verify=False)
    except Exception as e:
        raise
        return render_template('sys_error.html', error = error)
    reply = json.loads(response.content)
    for items in reply:
        ipadress = reply[count]['inet-address']['ip']
        name = reply[count]['name']
        dpid = reply[count]['dpid']
        state = reply[count]['fabric-connection-state']
        role = reply[count]['fabric-role']
        group = reply[count]['leaf-group']
        switch = [ipadress, name, dpid, state, role, group]
        switches.append(switch)
        count = count + 1
    return render_template('show_switch.html', switches = switches)

@app.route('/show_link', methods = ['GET'])
def show_link():
    error = None
    link = []
    links = []
    count = 0
    try:
        # path is set to substring "/api/v1/data/controller/applications/bcf/info/fabric/switch" from the above url
        path = '/api/v1/data/controller/applications/bcf/info/fabric?select=link'
        # we append this "show switch" path to the controller url to obtain a full url
        url = controller_url + path

        # There is no data to pass in for this GET request
        data = ''
        # the headers will contain the session cookie we obtained above via the POST request
        headers = {"content-type": "application/json", 'Cookie': session_cookie}

        response = requests.request('GET', url, data=data, headers=headers, verify=False)
    except Exception as e:
        raise
        return render_template('sys_error.html', error = error)
    reply = json.loads(response.content)
    total_links = reply[0]['link']
    for items in total_links:
        dintname = reply[0]['link'][count]['dst']['interface']['name']
        dintnum = reply[0]['link'][count]['dst']['interface']['number']
        dswitch = reply[0]['link'][count]['dst']['switch-info']['switch-name']
        linkdir = reply[0]['link'][count]['link-direction']
        linktype = reply[0]['link'][count]['link-type']
        sintname = reply[0]['link'][count]['src']['interface']['name']
        sintnum = reply[0]['link'][count]['src']['interface']['number']
        sswitch = reply[0]['link'][count]['src']['switch-info']['switch-name']
        link = [dintname, dintnum, dswitch, sintname, sintnum, sswitch, linkdir, linktype]
        links.append(link)
        count = count + 1
    return render_template('show_link.html', links = links)

@app.route('/show_portgroup', methods = ['GET'])
def show_portgroup():
    error = None
    group = []
    groups = []
    count = 0
    try:
        # path is set to substring "/api/v1/data/controller/applications/bcf/info/fabric/switch" from the above url
        path = '/api/v1/data/controller/applications/bcf/info/fabric/port-group'
        # we append this "show switch" path to the controller url to obtain a full url
        url = controller_url + path

        # There is no data to pass in for this GET request
        data = ''
        # the headers will contain the session cookie we obtained above via the POST request
        headers = {"content-type": "application/json", 'Cookie': session_cookie}

        response = requests.request('GET', url, data=data, headers=headers, verify=False)
    except Exception as e:
        raise
        return render_template('sys_error.html', error = error)
    reply = json.loads(response.content)
    for items in reply:
        tick = 0
        group_name = reply[count]['name']
        for ports in reply[count]['interface']:
            int_name = reply[count]['interface'][tick]['interface-name']
            leaf_group = reply[count]['interface'][tick]['leaf-group']
            switch_name = reply[count]['interface'][tick]['switch-name']
            state = reply[count]['interface'][tick]['state']
            tick = tick + 1
            group = [group_name, int_name, leaf_group, switch_name, state]
            groups.append(group)
        count = count + 1
    return render_template('show_group.html', groups = groups)

@app.route('/show_tenant', methods = ['GET'])
def show_tenant():
    error = None
    tenant = []
    tenants = []
    count = 0
    try:
        # path is set to substring "/api/v1/data/controller/applications/bcf/info/fabric/switch" from the above url
        path = '/api/v1/data/controller/applications/bcf/info/endpoint-manager/tenant'
        # we append this "show switch" path to the controller url to obtain a full url
        url = controller_url + path

        # There is no data to pass in for this GET request
        data = ''
        # the headers will contain the session cookie we obtained above via the POST request
        headers = {"content-type": "application/json", 'Cookie': session_cookie}

        response = requests.request('GET', url, data=data, headers=headers, verify=False)
    except Exception as e:
        raise
        return render_template('sys_error.html', error = error)
    reply = json.loads(response.content)
    for items in reply:
        name = reply[count]['name']
        endpoints = reply[count]['endpoint-count']
        ports = reply[count]['port-count']
        segments = reply[count]['segment-count']
        tenant = [name, endpoints, ports, segments]
        tenants.append(tenant)
        count = count + 1
    return render_template('show_tenant.html', tenants = tenants)

@app.route('/show_segment', methods = ['GET'])
def show_segment():
    error = None
    sement = []
    segments = []
    count = 0
    try:
        # path is set to substring "/api/v1/data/controller/applications/bcf/info/fabric/switch" from the above url
        path = '/api/v1/data/controller/applications/bcf/info/endpoint-manager/segment'
        # we append this "show switch" path to the controller url to obtain a full url
        url = controller_url + path

        # There is no data to pass in for this GET request
        data = ''
        # the headers will contain the session cookie we obtained above via the POST request
        headers = {"content-type": "application/json", 'Cookie': session_cookie}

        response = requests.request('GET', url, data=data, headers=headers, verify=False)
    except Exception as e:
        raise
        return render_template('sys_error.html', error = error)
    reply = json.loads(response.content)
    for items in reply:
        name = reply[count]['name']
        endpoints = reply[count]['endpoint-count']
        active = reply[count]['active-endpoint-count']
        vlan = reply[count]['internal-vlan']
        tenant = reply[count]['tenant']
        segment = [name, endpoints, active, vlan, tenant]
        segments.append(segment)
        count = count + 1
    return render_template('show_segment.html', segments = segments)

@app.route('/add_tenant', methods=['POST', 'GET'])
def add_tenant():
    error = None
    if request.method == 'POST':
        tenant = request.form.get('tenant')
        path = '/api/v1/data/controller/applications/bcf/tenant[name="%s"]' % tenant
        url = controller_url + path
        data = '{"name": "%s"}' % tenant
        headers = {"content-type": "application/json", 'Cookie': session_cookie}
        try:
            response = requests.request('PUT', url, data=data, headers=headers, verify=False)
        except Exception as e:
            raise
            return render_template('sys_error.html', error = error)
        return render_template('success.html')
    return render_template('add_tenant.html')

@app.route('/add_portgroup', methods=['POST', 'GET'])
def add_portgroup():
    error = None
    if request.method == 'POST':
        portgroup = request.form.get('portgroup')
        path = '/api/v1/data/controller/applications/bcf/port-group[name="%s"]' % portgroup
        url = controller_url + path
        data = '{"name": "%s"}' % portgroup
        headers = {"content-type": "application/json", 'Cookie': session_cookie}
        try:
            response = requests.request('PUT', url, data=data, headers=headers, verify=False)
        except Exception as e:
            raise
            return render_template('sys_error.html', error = error)
        return render_template('success.html')
    return render_template('add_portgroup.html')

@app.route('/add_int2pg', methods=['POST', 'GET'])
def add_int2pg():
    error = None
    if request.method == 'POST':
        return render_template('success.html')
    return render_template('add_int2pg.html')

@app.route('/add_pg2seg', methods=['POST', 'GET'])
def add_pg2seg():
    error = None
    if request.method == 'POST':
        return render_template('success.html')
    return render_template('add_pg2seg.html')

@app.route('/add_pgs2seg', methods=['POST', 'GET'])
def add_pgs2seg():
    error = None
    if request.method == 'POST':
        return render_template('success.html')
    return render_template('add_pgs2seg.html')

@app.route('/add_segment', methods=['POST', 'GET'])
def add_segment():
    error = None
    if request.method == 'POST':
        return render_template('success.html')
    return render_template('add_segment.html')

@app.route('/add_ints2pg', methods = ['GET', 'POST'])
def add_ints2pg():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('chooser.html')
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('chooser.html')
        #if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        vars = {}
        cr ='\n'
        with open(os.path.join(APP_STATIC, filename)) as f:
            line = f.readline().strip('/t')
            while line:
                vars = str.split(line, ',')
                # assign the variables from the linf of the csv file
                port_group = vars[0]
                switch = vars[1]
                interface = vars[2]
                # Check for unwanted data
                if port_group == 'Port Group':
                    break
                if port_group == 'eof':
                    break
                path = '/api/v1/data/controller/applications/bcf/port-group  \
                    [name="%s"]/member-interface[switch-name="%s"][interface-name="%s"]' % (port_group, switch, interface)
                data = '{"switch-name": "%s", "interface-name": "%s"}' % (switch, interface)
                headers = {"content-type": "application/json", 'Cookie': session_cookie}
                try:
                    response = requests.request('PUT', url, data=data, headers=headers, verify=False)
                except Exception as e:
                    raise
                    return render_template('sys_error.html', error = error)
                line = f.readline().strip('/t')
                #time.sleep(5)

        f.close()
        flash('Records processed')
        return render_template('success.html')
    return render_template('chooser.html')


@app.route('/logout')
def logout():
    error = None
    ##################################
    # Logout
    ##################################
    path = '/api/v1/data/controller/core/aaa/session[auth-token="'+cookie+'"]'
    url = controller_url + path
    headers = {"content-type": "application/json", 'Cookie': session_cookie}
    # DELETE request made on the Big Cloud Fabric controller
    response = requests.request('DELETE', url, headers=headers, verify=False)
    flash('You are now logged out of the applcation')
    return render_template('main.html', error = error)


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return redirect('http://www.wookieware.com')


if __name__ == '__main__':
    #db.create_all()
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')
