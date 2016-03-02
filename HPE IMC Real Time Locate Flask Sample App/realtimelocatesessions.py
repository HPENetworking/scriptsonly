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
        locations = get_real_time_locate(request.form.get('host'), auth=auth, url=session['url'])
        
        if len(locations) < 1 :
            error = 'Unable to find host'
            return render_template('realtimelocate.html', error=error)

        devicedetailsList=[]
        locationDataList=[]
        for location in locations:
            devicedetails = get_dev_details(location['deviceIp'], auth=auth, url=session['url'])
            devicedetailsList.append(devicedetails)
            locationData=dict(location)
            locationData.update(devicedetails)
            locationDataList.append(locationData)

        flash("Host Located")
        flash("Proof of Concept Real-Time Location App")

        session['hosts'] = locations
        session['devices'] = devicedetailsList
        session['locationDataList'] = locationDataList

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
            for host in session['hosts']:
                set_inteface_down(devid=host['deviceId'],ifindex=host['ifIndex'],auth=auth,url=session['url'])
                flash("Port " +  host['ifDesc'] + " State Changed to Admin Down")
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'])
        elif request.form['action'] == 'up':
            for host in session['hosts']:
                set_inteface_up(devid=host['deviceId'],ifindex=host['ifIndex'],auth=auth,url=session['url'])
                flash('Port ' +  host['ifDesc'] +' State Changed to Admin Up')
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'])
        elif request.form['action'] == 'epoe':
            for host in session['hosts']:
                cmd_list = ['system-view', 'interface '+ host['ifDesc'], 'poe enable']
                run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
                flash("PoE Enabled on Interface " +  host['ifDesc'])
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'])
        elif request.form['action'] == 'dpoe':
            for host in session['hosts']:
                cmd_list = ['system-view', 'interface '+host['ifDesc'], 'undo poe enable']
                run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
                flash("PoE Disabled on Interface " +  host['ifDesc'])
            return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'])

        #Get Interface Information Section
        elif request.form['action'] == 'macq':
            #cmd_list = ['system-view', 'display mac-address interface ' + session['host']['ifDesc']]
            #session['macq'] = run_dev_cmd(devid=session['host']['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] )
            #if neighbor['success'] is 'true':
            redirect(url_for('macquery'))
            #return render_template('macquery.html',url=session['url'], username=session['username'], password=session['password']
                       #    , host=session['host'], device=session['device'],macq = macq )

        elif request.form['action'] == 'stats':
            instats = []
            for host in session['hosts']:
                cmd_list = ['display interface ' + host['ifDesc']]
                instats.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
            return render_template('intstats.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'], intstats=instats)

        elif request.form['action'] == 'lldp':
            neighbors=[]
            for host in session['hosts']:
                cmd_list = ['display lldp neigh interface ' + host['ifDesc']]
                neighbors.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
            #if neighbor['success'] is 'true':
            return render_template('lldpneigh.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],neighbors = neighbors )

        elif request.form['action'] == 'arpq':
            arpq = []
            for host in session['hosts']:
                cmd_list = ['display arp interface ' + host['ifDesc']]
                arpq.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
            #if neighbor['success'] is 'true':
            return render_template('arpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],arpq = arpq )
        elif request.form['action'] == 'stpq':
            stpq = []
            for host in session['hosts']:
                cmd_list = ['display stp interface ' + host['ifDesc']]
                stpq.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
            #if neighbor['success'] is 'true':
            return render_template('stpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],stpq = stpq )
    if 'login' not in session:
        error = "User not logged in"
        return render_template('login.html', error=error)

#    return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
#                           , host=session['host'], device=session['device'])

    return render_template('results.html', url=session['url'], username=session['username'], password=session['password']
                               , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'])



#The following section respond to buttons pushed on the results page

@app.route('/intstats', methods=['GET', 'POST'])
def instats():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    instats = []
    for host in session['hosts']:
        cmd_list = ['display interface ' + host['ifDesc']]
        instats.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
    return render_template('intstats.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'], intstats=instats)

@app.route('/stpinfo', methods=['GET', 'POST'])
def stpinfo():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    stpinfo = []
    for host in session['hosts']:
        cmd_list = ['display stp interface ' + host['ifDesc']]
        stpinfo.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
    return render_template('stpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],stpq = stpinfo )

@app.route('/arpquery', methods = ['GET', 'POST'])
def arpquery():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    arpq = []
    for host in session['hosts']:
        cmd_list = ['display arp interface ' + host['ifDesc']]
        arpq.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
    return render_template('arpquery.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],arpq = arpq )


@app.route('/macquery', methods=['GET', 'POST'])
def macquery():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    session['macq'] = []
    for host in session['hosts']:
        cmd_list = ['display mac-address interface ' + host['ifDesc']]
        session['macq'].append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url']))
    return render_template('macquery.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],macq = session['macq'] )


@app.route('/lldpneigh', methods=['GET', 'POST'])
def lldpneigh():
    auth = requests.auth.HTTPDigestAuth(session['username'],session['password'])
    neighbors=[]
    for host in session['hosts']:
        cmd_list = ['display lldp neigh interface ' + host['ifDesc']]
#        cmd_list = ['display lldp neigh list | i ' + host['ifDesc']]
        neighbors.append(run_dev_cmd(devid=host['deviceId'],cmd_list=cmd_list, auth=auth, url=session['url'] ))
    return render_template('lldpneigh.html',url=session['url'], username=session['username'], password=session['password']
                           , hosts=session['hosts'], devices=session['devices'], locationDataList=session['locationDataList'],neighbors = neighbors )




if __name__ == '__main__':
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')

