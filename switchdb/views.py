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

Flask script that launches switchdb
06282016 RAK added file downloader

'''

from flask import Flask, request, render_template, redirect, url_for, flash, session, send_file
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Switches
from settings import APP_STATIC
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = APP_STATIC
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)

# Verify extension is csv only
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Routes
# Main Menu
@app.route('/')
@app.route('/index')
def show_all():
    return render_template('show_all.html', switches = Switches.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['mac'] or not request.form['sysname'] or not request.form['tftpserver']:
         flash('Please enter all the fields', 'error')
      else:

         check1 =Switches.query.filter_by(mac=request.form['mac']).all()
         check2 =Switches.query.filter_by(sysname=request.form['sysname']).all()
         check3 =Switches.query.filter_by(mgmt_ip=request.form['mgmt_ip']).all()

         if check1 or check2 or check3:
             flash('Database Error...duplicate records', 'error')
         else:
              switches = Switches(request.form['mac'],request.form['sysname'],
                 request.form['mgmt_ip'],request.form['mgmt_sub'],request.form['gateway'],
                    request.form['fanDirection'],request.form['localuser'],
                        request.form['passwd'],request.form['tftpserver'],request.form['rolex'])
              db.session.add(switches)
              db.session.commit()
              flash('Record was successfully added')
              return redirect(url_for('show_all'))

   return render_template('new.html')

# Select record for editing
@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':
        check1 =Switches.query.filter_by(sysname=request.form['sysname']).all()
        if check1:
            return render_template('show_edit.html', switch = check1)
        else:
            flash('Database Error...sysname not found', 'error')
    return render_template('edit_select.html')


# Save record after editing
@app.route('/editsave', methods = ['POST'])
def editsave():
    switch = Switches.query.filter_by(sysname=request.form['sysname']).all()
    switch[0].mac = request.form['mac']
    switch[0].sysname = request.form['sysname']
    switch[0].mgmt_ip = request.form['mgmt_ip']
    switch[0].mgmt_sub = request.form['mgmt_sub']
    switch[0].gateway = request.form['gateway']
    switch[0].fanDirection = request.form['fanDirection']
    switch[0].localuser = request.form['localuser']
    switch[0].passwd = request.form['passwd']
    switch[0].tftpserver = request.form['tftpserver']
    switch[0].rolex = request.form['rolex']
    try:
        db.session.commit()
        flash('Record was successfully saved')
        return redirect(url_for('show_all'))
    except:
        db.session.rollback()
        flash('Datbase Rollback changes not saved')
        return redirect(url_for('show_all'))

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        check1 =Switches.query.filter_by(sysname=request.form['sysname']).all()
        if check1:
            try:
                switch = Switches.query.filter_by(sysname=request.form['sysname']).delete()
                db.session.commit()
                flash('Record was successfully deleted')
                return redirect(url_for('show_all'))
            except:
                db.session.rollback()
                flash('Failed to update record!!!!')
                return render_template('del_select.html')
        flash('Record not found in database')
        return render_template('del_select.html')

    return render_template('del_select.html')

# List all records
@app.route('/list', methods = ['GET', 'POST'])
def list():
    if request.method == 'POST':
        return redirect(url_for('show_all'))
    return render_template('list.html', switches = Switches.query.all() )

# Bulk import from file selector
@app.route('/bulk', methods = ['GET', 'POST'])
def bulk():
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
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            vars = {}
            success = 0
            fail = 0
            with open(os.path.join(APP_STATIC, filename)) as f:
                line = f.readline().strip('/t')
                while line:
                    vars = str.split(line, ',')
                    switches = Switches(vars[0],vars[1],vars[2],vars[3],vars[4],
                        vars[5],vars[6],vars[7],vars[8],vars[9])
                    # Check for database duplicates
                    check1 =Switches.query.filter_by(mac=vars[0]).all()
                    check2 =Switches.query.filter_by(sysname=vars[1]).all()
                    check3 =Switches.query.filter_by(mgmt_ip=vars[2]).all()
                    if check1 or check2 or check3:
                        fail = fail + 1
                        line = f.readline().strip('/t')
                    else:
                        db.session.add(switches)
                        db.session.commit()
                        success = success + 1
                        line = f.readline().strip('/t')

            f.close()
            flash('Records processed')
            f = open(os.path.join(APP_STATIC, 'switchdb.csv'), 'r')
            filex = f.read()
            return render_template('bulk.html', success = success, fail= fail, filex = filex)
            f.close()
    return render_template('chooser.html')

# Generate Ansible file
@app.route('/generate', methods = ['GET', 'POST'])
def generate():
    counter = 0
    cr ='\n'
    switch = Switches.query.all()
    f = open(os.path.join(APP_STATIC, 'varMatrix.yaml'), 'w')
    line = "---"
    f.write(line)
    f.write(cr)
    while (counter < len(switch)):
        line = " "+switch[counter].mac+":"
        f.write(line)
        f.write(cr)
        line = "   sysname: " + switch[counter].sysname
        f.write(line)
        f.write(cr)
        line = "   mgmt_ip: " + switch[counter].mgmt_ip
        f.write(line)
        f.write(cr)
        line = "   mgmt_subnet: " + switch[counter].mgmt_sub
        f.write(line)
        f.write(cr)
        line = "   gateway: " + switch[counter].gateway
        f.write(line)
        f.write(cr)
        line = "   fanDirection: " + switch[counter].fanDirection
        f.write(line)
        f.write(cr)
        line = "   local_user: " + switch[counter].localuser
        f.write(line)
        f.write(cr)
        line = "   passwd: " + switch[counter].passwd
        f.write(line)
        f.write(cr)
        line = "   tftpserver: " + switch[counter].tftpserver
        f.write(line)
        f.write(cr)
        line = "   role: " + switch[counter].rolex
        f.write(line)
        f.write(cr)
        counter = counter + 1
    f.close()
    f = open(os.path.join(APP_STATIC, 'varMatrix.yaml'), 'r')
    file = f.read()
    f.close()
    flash('Ansible variable file has been created in /static/varMatrix.yaml')
    return render_template('generate_vars.html', file = file)

# Generate Ansible file
@app.route('/genjson', methods = ['GET', 'POST'])
def genjson():
    counter = 0
    cr ='\n'
    switch = Switches.query.all()
    eof = (len(switch) -1)
    f = open(os.path.join(APP_STATIC, 'varMatrix.json'), 'w')
    line = "{"
    f.write(line)
    f.write(cr)
    while (counter < len(switch)):
        line = '    "'+switch[counter].mac+'":{'
        f.write(line)
        f.write(cr)
        line = '        "sysname": ' + '"'+switch[counter].sysname+'",'
        f.write(line)
        f.write(cr)
        line = '        "mgmt_ip": ' + '"'+switch[counter].mgmt_ip+'",'
        f.write(line)
        f.write(cr)
        line = '        "mgmt_sub": ' + '"'+switch[counter].mgmt_sub+'",'
        f.write(line)
        f.write(cr)
        line = '        "gateway": ' + '"'+switch[counter].gateway+'",'
        f.write(line)
        f.write(cr)
        line = '        "fanDirection": ' + '"'+switch[counter].fanDirection+'",'
        f.write(line)
        f.write(cr)
        line = '        "localuser": ' + '"'+switch[counter].localuser+'",'
        f.write(line)
        f.write(cr)
        line = '        "passwd": ' + '"'+switch[counter].passwd+'",'
        f.write(line)
        f.write(cr)
        line = '        "tftpserver": ' + '"'+switch[counter].tftpserver+'",'
        f.write(line)
        f.write(cr)
        line = switch[counter].rolex.strip()
        line = '        "rolex": ' + '"'+ line +'"'
        f.write(line)
        f.write(cr)
        if (eof == counter):
            line ='     }'
        else:
            line ='    },'
        f.write(line)
        f.write(cr)
        counter = counter + 1
    line = "}"
    f.write(line)
    f.write(cr)
    f.close()
    f = open(os.path.join(APP_STATIC, 'varMatrix.json'), 'r')
    file = f.read()
    f.close()
    flash('JSON formatted variable file has been created in /static/varMatrix.json')
    return render_template('generate_json.html', file = file)

# Generate Ansible file
@app.route('/dbdump', methods = ['GET', 'POST'])
def dbdump():
    counter = 0
    cr ='\n'
    switch = Switches.query.all()
    f = open(os.path.join(APP_STATIC, 'switchdb.csv'), 'w')
    while (counter < len(switch)):
        line = switch[counter].mac+','+switch[counter].sysname+','+switch[counter].mgmt_ip+','+ \
            switch[counter].mgmt_sub+','+switch[counter].gateway+','+switch[counter].fanDirection \
                +','+switch[counter].localuser+','+switch[counter].passwd+','+  \
                    switch[counter].tftpserver+','+switch[counter].rolex
        f.write(line)
        counter = counter + 1
    f.close()
    flash('Datbase dumped to file /static/switchdb.csv')
    return render_template('dbdump.html')

@app.route('/dbdelete', methods = ['GET', 'POST'])
def dbdelete():
    return render_template('dbdelete.html')

@app.route('/killthemall', methods = ['GET', 'POST'])
def killthemall():
    counter = 0
    switch = Switches.query.all()
    while (counter < len(switch)):

        try:
            db.session.delete(switch[counter])
            db.session.commit()
        except:
            db.session.rollback()
        counter = counter + 1

    flash('All record have been removed')
    return render_template('dbkilldone.html')

@app.route('/logout')
def logout():
    #session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return redirect('http://www.wookieware.com')

# Version 0.2 additions..send csv template for bulk uploads
@app.route('/filedownloads')
def filedownloads():
    file = os.path.join(APP_STATIC, 'switchdb.csv')
    return send_file(file)


if __name__ == '__main__':
    db.create_all()
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')
