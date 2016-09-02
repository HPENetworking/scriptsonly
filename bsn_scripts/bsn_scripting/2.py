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

test connectivity to the VSD API
'''

def ftc(fahrenheit):
    global centigrade
    centigrade = (fahrenheit-32) * (5.0/9.0)
    return (centigrade)
PI = 3.141592

def circle_area(r):
    return PI*r*r

def log():
    user = 'rick kauffman'
    return (user, centigrade)

print circle_area(5)

print ftc(45)

print log()

test = log()

print test
