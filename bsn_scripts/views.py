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
    return render_template('show_link.html', response = response.content)

@app.route('/show_portgroup', methods = ['GET'])
def show_portgroup():
    error = None
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
    return render_template('show_group.html', response = response.content)

@app.route('/show_tenant', methods = ['GET'])
def show_tenant():
    error = None
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
    return render_template('show_tenant.html', response = response.content)

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
