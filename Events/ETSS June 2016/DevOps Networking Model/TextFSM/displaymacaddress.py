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





displaymadaddress = """<5900>displa mac-address
MAC Address      VLAN ID    State            Port/NickName            Aging
001e-c1dc-fc01   1          Learned          XGE1/0/47                Y
2c23-3a40-7e18   1          Learned          XGE1/0/48                Y
2c23-3a40-7e4e   1          Learned          XGE1/0/48                Y
<5900>"""



template = open("./templates/displaymadaddress.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displaymadaddress)

for i in fsm_results:
    print (i)