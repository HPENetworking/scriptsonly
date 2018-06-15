#!/usr/bin/env python
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


__author__ = "@netwookie"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Flask script that launches switchdb

'''

from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Switches

app = Flask(__name__)

bootstrap = Bootstrap(app)

# Routes

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

@app.route('/edit', methods = ['GET', 'POST'])

# Select record for editing
def edit():
    if request.method == 'POST':
        switch = Switches.query.filter_by(sysname=request.form['sysname']).all()
        return render_template('show_edit.html', switch = switch)

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
        try:
            switch = Switches.query.filter_by(sysname=request.form['sysname']).delete()
            db.session.commit()
            flash('Record was successfully deleted')
            return redirect(url_for('show_all'))
        except:
            db.session.rollback()
            flash('Failed to update record!!!!')
            return redirect(url_for('show_all'))


    return render_template('del_select.html')

# List all records
@app.route('/list', methods = ['GET', 'POST'])
def list():
    if request.method == 'POST':
        return redirect(url_for('show_all'))
    return render_template('list.html', switches = Switches.query.all() )




@app.route('/logout')
def logout():
    #session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')
