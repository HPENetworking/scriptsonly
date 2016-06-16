''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
import jtextfsm as textfsm
import json


displaylldpneigh = '''5900>dis lldp neighbor-information
LLDP neighbor-information of port 47[Ten-GigabitEthernet1/0/47]:
LLDP agent nearest-bridge:
 LLDP neighbor index : 1
 ChassisID/subtype   : 001e-c1dc-fc00/MAC address
 PortID/subtype      : GigabitEthernet2/0/23/Interface name
 Capabilities        : Bridge, Router

LLDP neighbor-information of port 48[Ten-GigabitEthernet1/0/48]:
LLDP agent nearest-bridge:
 LLDP neighbor index : 1
 ChassisID/subtype   : 2c23-3a40-7e0e/MAC address
 PortID/subtype      : GigabitEthernet1/0/24/Interface name
 Capabilities        : Bridge, Router, Customer Bridge

LLDP neighbor-information of port 16771[M-GigabitEthernet0/0/0]:
LLDP agent nearest-bridge:
 LLDP neighbor index : 1
 ChassisID/subtype   : 001e-c1dc-fc00/MAC address
 PortID/subtype      : GigabitEthernet1/0/22/Interface name
 Capabilities        : Bridge, Router

<5900>'''


template = open("./templates/displaylldpneigh.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displaylldpneigh)


print (fsm_results)