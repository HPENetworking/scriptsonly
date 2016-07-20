''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm


 Copyright 2016 Hewlett Packard Enterprise Development LP.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''
import jtextfsm as textfsm
import json
import os



displayclock = """<5900>display clock
19:35:31 UTC Sat 01/08/2011
<5900>"""

displayclockCW5 = '''<HP_5500EI>display clock
17:10:18 UTC Fri 06/17/2016
<HP_5500EI>'''

template = open("./templates/displayclock.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displayclock)


print (fsm_results)
re_table = textfsm.TextFSM(template)
fsm_results2 = re_table.ParseText(displayclockCW5)

print (fsm_results2)
