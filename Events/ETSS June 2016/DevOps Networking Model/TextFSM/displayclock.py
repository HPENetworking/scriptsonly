''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
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
