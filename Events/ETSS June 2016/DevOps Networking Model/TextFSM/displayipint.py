
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