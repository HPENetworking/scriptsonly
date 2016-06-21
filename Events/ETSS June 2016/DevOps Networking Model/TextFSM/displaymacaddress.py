''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
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