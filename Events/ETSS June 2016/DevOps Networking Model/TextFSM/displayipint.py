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



cw7 = '''<5900>dis ip int br
*down: administratively down
(s): spoofing
Interface                     Physical Protocol IP Address      Description
M-GE0/0/0                     up       up       10.20.10.10     M-Gigabit...
Vlan1                         up       up       10.20.1.1       Vlan-inte...
<5900>'''



template = open("./templates/displayipintbrief.testfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(cw7)



print (json.dumps(fsm_results, indent=4))