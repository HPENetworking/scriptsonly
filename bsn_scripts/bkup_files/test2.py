from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response
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

bootstrap = Bootstrap(app)# Generate Ansible file
switch = Switches.query.all()
lenx = (len(switch) -1)
line = switch[0].rolex.strip()
line = '    "rolex": ' + '"'+ line +'",'
print line
print lenx
