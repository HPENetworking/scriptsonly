''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
import jtextfsm as textfsm
import json
import os



dispaysnmpcommunity = """<5900>display snmp community
   Community name: private
       Group name: private
       Storage-type: nonVolatile

   Community name: public
       Group name: public
       Storage-type: nonVolatile

<5900>"""


template = open("./templates/dispaysnmpcommunity.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(dispaysnmpcommunity)

for i in fsm_results:
    print (i)