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

switchdb  A database tool for managing switches in the Ansible VAR file

'''

from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sdb_maker import db
from sdb_maker import Students

app = Flask(__name__)

bootstrap = Bootstrap(app)



# Moving on

@app.route('/')
@app.route('/index')
def show_all():
    return render_template('show_all.html', students = Students.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = Students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])

         db.session.add(student)
         db.session.commit()

         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')




if __name__ == '__main__':
    db.create_all()
    app.secret_key = 'SuperSecret'
    app.debug = True
    app.run(host='0.0.0.0')
