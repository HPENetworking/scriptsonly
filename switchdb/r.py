
from flask import Flask
from settings import APP_STATIC
import os

app = Flask(__name__)


f = os.path.join(APP_STATIC, 'varMatrix.yaml')
print f

#with open(os.path.join(APP_STATIC, 'switchdb.csv')) as f:
