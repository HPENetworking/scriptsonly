'''
 Copyright 2016 Hewlett Packard Enterprise Development LP.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netmanchris"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Chris Young"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Chris Young"
__email__ = "chris_young@me.com"
__status__ = "Prototype"

'''

from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask.ext.bootstrap import Bootstrap
from pyhpeimc.auth import *
from pyhpeimc.plat.device import *
from pyhpeimc.plat.termaccess import *


app = Flask(__name__)
bootstrap = Bootstrap(app)


#index file
@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        auth= IMCAuth("http://",
                      request.form.get('ipaddress'),
                      request.form.get('port'),
                      request.form.get('username'),
                      request.form.get('password'))
        test_creds = test_imc_creds(auth=auth.creds, url=auth.url)
        if test_creds == True:
            session['username'] = request.form.get('username')
            session['password'] = auth.password
            session['url'] = auth.url
            session['login'] = 'True'
            flash('authentication successful')
            return redirect(url_for('locate'))
        else:
            error = "Incorrect username and password"
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('host', None)
    session.pop('login', None)
    return redirect(url_for('login'))


@app.route('/locate', methods=['GET', 'POST'])
def locate():
    error = None
    if request.method == "POST":
        auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
        location = get_real_time_locate(request.form.get('host'), auth=auth, url=session['url'])
        if len(location) < 1 :
            error = 'Unable to find host'
            return render_template('realtimelocate.html', error=error)
        devicedetails = get_dev_details(location['deviceIp'], auth=auth, url=session['url'])
        flash("Host Located")
        flash("Proof of Concept Real-Time Location App")
        session['host'] = location
        session['device'] = devicedetails
        return redirect(url_for('results'))
    if 'login' not in session:
        error = "User not logged in"
        return render_template('login.html', error=error)
    return render_template('realtimelocate.html', error=error)


@app.route('/results', methods =['GET', 'POST'])
def results():
    error = None
    if request.method == 'POST':
        auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
        #Take Action on Interface Information Section
        if request.form['action'] == 'down':
            set_inteface_down(devid=session['host']['deviceId'],ifindex=session['host']['ifIndex'],auth=auth,url=session['url'])
            flash("Port State Changed to Admin Down")
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'])
        elif request.form['action'] == 'up':
            set_inteface_up(devid=session['host']['deviceId'],ifindex=session['host']['ifIndex'],auth=auth,url=session['url'])
            flash('Port State Changed to Admin Up')
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'])
        elif request.form['action'] == 'epoe':
            cmd_list = ['system-view', 'interface '+ session['host']['ifDesc'], 'poe enable']
            run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            flash("PoE Enabled on Interface" +  session['host']['ifDesc'])
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'])
        elif request.form['action'] == 'dpoe':
            cmd_list = ['system-view', 'interface '+session['host']['ifDesc'], 'undo poe enable']
            run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            flash("PoE Disabled on Interface" +  session['host']['ifDesc'])
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'])

        #Get Interface Information Section
        elif request.form['action'] == 'macq':
            #cmd_list = ['system-view', 'display mac-address interface ' + session['host']['ifDesc']]
            #session['macq'] = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            #if neighbor['success'] is 'true':
            redirect(url_for('macquery'))
            #return render_template('macquery.html',url=session['url'], username=session['username'], password=session['password']
                       #    , host=session['host'], device=session['device'],macq = macq )

        elif request.form['action'] == 'stats':
            cmd_list = ['system-view', 'display interface ' + session['host']['ifDesc']]
            instats = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            return render_template('intstats.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'], intstats=instats)

        elif request.form['action'] == 'lldp':
            cmd_list = ['system-view', 'display lldp neigh interface ' + session['host']['ifDesc']]
            neighbor = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            #if neighbor['success'] is 'true':
            return render_template('lldpneigh.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],neighbor = neighbor )

        elif request.form['action'] == 'arpq':
            cmd_list = ['system-view', 'display arp interface ' + session['host']['ifDesc']]
            arpq = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            #if neighbor['success'] is 'true':
            return render_template('arpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],arpq = arpq )
        elif request.form['action'] == 'stpq':
            cmd_list = ['system-view', 'display stp interface ' + session['host']['ifDesc']]
            arpq = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            #if neighbor['success'] is 'true':
            return render_template('stpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],stpq = arpq )
    if 'login' not in session:
        error = "User not logged in"
        return render_template('login.html', error=error)
    return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'])


#The following section respond to buttons pushed on the results page

@app.route('/intstats', methods=['GET', 'POST'])
def instats():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    cmd_list = ['system-view', 'display interface ' + session['host']['ifDesc']]
    instats = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
    return render_template('intstats.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'], intstats=instats)

@app.route('/stpinfo', methods=['GET', 'POST'])
def stpinfo():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    cmd_list = ['system-view', 'display stp interface ' + session['host']['ifDesc']]
    stpinfo = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
    return render_template('stpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],stpq = stpinfo )

@app.route('/arpquery', methods = ['GET', 'POST'])
def arpquery():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    cmd_list = ['system-view', 'display arp interface ' + session['host']['ifDesc']]
    arpq = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
    return render_template('arpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],arpq = arpq )


@app.route('/macquery', methods=['GET', 'POST'])
def macquery():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    cmd_list = ['system-view', 'display mac-address interface ' + session['host']['ifDesc']]
    session['macq'] = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'])

    return render_template('macquery.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],macq = session['macq'] )


@app.route('/lldpneigh', methods=['GET', 'POST'])
def lldpneigh():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    cmd_list = ['system-view', 'display lldp neigh interface ' + session['host']['ifDesc']]
    neighbor = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
    return render_template('lldpneigh.html',url=session['url'], username=session['username'], password=session['password']
                           , host=session['host'], device=session['device'],neighbor = neighbor )




if __name__ == '__main__':
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')

