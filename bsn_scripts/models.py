
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

Script builds database for switchdb

'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import APP_ROOT
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(APP_ROOT,'switchdb.db')
db = SQLAlchemy(app)

# need to  ID unique fields
class Switches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(20),unique=True)
    sysname = db.Column(db.String(20),unique=True)
    mgmt_ip = db.Column(db.String(20),unique=True)
    mgmt_sub = db.Column(db.String(20))
    gateway = db.Column(db.String(20))
    fanDirection = db.Column(db.String(20))
    localuser = db.Column(db.String(50))
    passwd = db.Column(db.String(50))
    tftpserver = db.Column(db.String(20))
    rolex = db.Column(db.String(20))

    # Maybe do def __init__(self, * args, **kwargs):
    def __init__(self, mac, sysname, mgmt_ip, mgmt_sub, gateway, fanDirection, localuser, passwd, tftpserver, rolex):
    #def __init__(self, *args, **kwargs):
        self.mac = mac
        self.sysname = sysname
        self.mgmt_ip = mgmt_ip
        self.mgmt_sub = mgmt_sub
        self.gateway = gateway
        self.fanDirection = fanDirection
        self.localuser = localuser
        self.passwd = passwd
        self.tftpserver = tftpserver
        self.rolex = rolex

    def __repr__(self):
        #return '<Switches %r>' % self.sysname

        return '<Switches %r>' % self.mac, self.sysname, self.mgmt_ip, self.mgmt_sub, self.gateway, self.fanDirection, \
            self.localuser, self.passwd, self.tftpserver, self.rolex
