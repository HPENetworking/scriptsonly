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

displaylldpneighverbose = '''<5900>dis lldp neigh verbose
LLDP neighbor-information of port 47[Ten-GigabitEthernet1/0/47]:
LLDP agent nearest-bridge:
 LLDP neighbor index : 1
 Update time         : 0 days, 0 hours, 2 minutes, 15 seconds
 Chassis type        : MAC address
 Chassis ID          : 001e-c1dc-fc00
 Port ID type        : Interface name
 Port ID             : GigabitEthernet2/0/23
 Time to live        : 120
 Port description    : GigabitEthernet2/0/23 Interface
 System name         : HP_5500EI
 System description  : HP Comware Platform Software, Software Version 5.20.99 Re
                       lease 2221P20
                       HP A5500-24G-PoE+ EI Switch with 2 Interface Slots
                       Copyright (c) 2010-2015 Hewlett Packard Enterprise Develo
                       pment LP
 System capabilities supported : Bridge, Router
 System capabilities enabled   : Bridge, Router
 Management address type           : IPv4
 Management address                : 10.20.1.254
 Management address interface type : IfIndex
 Management address interface ID   : 85
 Management address OID            : 0
 Link aggregation supported : Yes
 Link aggregation enabled   : No
 Aggregation port ID        : 0
 Auto-negotiation supported : Yes
 Auto-negotiation enabled   : Yes
 OperMau                    : Speed(1000)/Duplex(Full)
 Power port class           : PSE
 PSE power supported        : Yes
 PSE power enabled          : No
 PSE pairs control ability  : No
 Power pairs                : Signal
 Port power classification  : Class 0
 Maximum frame size         : 9216

LLDP neighbor-information of port 16771[M-GigabitEthernet0/0/0]:
LLDP agent nearest-bridge:
 LLDP neighbor index : 1
 Update time         : 0 days, 0 hours, 2 minutes, 17 seconds
 Chassis type        : MAC address
 Chassis ID          : 001e-c1dc-fc00
 Port ID type        : Interface name
 Port ID             : GigabitEthernet1/0/22
 Time to live        : 120
 Port description    : GigabitEthernet1/0/22 Interface
 System name         : HP_5500EI
 System description  : HP Comware Platform Software, Software Version 5.20.99 Re
                       lease 2221P20
                       HP A5500-24G-PoE+ EI Switch with 2 Interface Slots
                       Copyright (c) 2010-2015 Hewlett Packard Enterprise Develo
                       pment LP
 System capabilities supported : Bridge, Router
 System capabilities enabled   : Bridge, Router
 Management address type           : IPv4
 Management address                : 10.20.10.1
 Management address interface type : IfIndex
 Management address interface ID   : 22
 Management address OID            : 0
 Link aggregation supported : Yes
 Link aggregation enabled   : No
 Aggregation port ID        : 0
 Auto-negotiation supported : Yes
 Auto-negotiation enabled   : Yes
 OperMau                    : Speed(1000)/Duplex(Full)
 Power port class           : PSE
 PSE power supported        : Yes
 PSE power enabled          : No
 PSE pairs control ability  : No
 Power pairs                : Signal
 Port power classification  : Class 0
 Maximum frame size         : 9216

<5900>'''






template = open("./templates/displaylldpneighverbose.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displaylldpneighverbose)


print (len(fsm_results))

for neighbor in fsm_results:
    print (neighbor)




