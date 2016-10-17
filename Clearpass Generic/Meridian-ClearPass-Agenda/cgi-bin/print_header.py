#!/usr/bin/env python3
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


__author__ = "@netmanfabe"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Fabien GIRAUD"]
__license__ = "Apache2"
__version__ = "2.0.0"
__maintainer__ = "Fabien GIRAUD"
__email__ = "fabien_giraud@me.com"
__status__ = "Prototype"

'''
# Script for debugging in the Meridian APP (in order to see the headers)
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import json
import re

print('Content-type: application/json')
print('')

import os

print(os.environ)

print("<h2>Authorization Header: </h2>")
#print(cgi.parse_header('HTTP_AUTHORIZATION'))
print (os.environ['HTTP_AUTHORIZATION'])
token=re.sub('Bearer ','',os.environ['HTTP_AUTHORIZATION'])
print("<H2>Token</H2>")
print(token)

#print("<h2>URI Parameter 'token'</h2>")
#print(cgi.FieldStorage()["token"].value)
