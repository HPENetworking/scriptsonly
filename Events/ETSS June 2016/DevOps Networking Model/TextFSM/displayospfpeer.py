
import jtextfsm as textfsm
import json


raw_text_data = """<HP_5500EI>dis ospf peer

	          OSPF Process 1 with Router ID 10.101.0.221
                        Neighbor Brief Information

 Area: 0.0.0.0
 Router ID       Address         Pri  Dead-Time  Interface       State
 10.101.16.1     10.101.0.1      1    34         Vlan1           Full/BDR
 10.254.0.100    10.10.10.30     1    37         Vlan10          Full/BDR
 10.101.16.1     10.101.15.1     1    38         Vlan15          Full/BDR
 10.20.1.1       10.20.1.1       1    32         GE2/0/23        Full/BDR"""



vlan = '''<5900>display vlan brief
Brief information about all VLANs:
Supported Minimum VLAN ID: 1
Supported Maximum VLAN ID: 4094
Default VLAN ID: 1
VLAN ID   Name                             Port
1         VLAN 0001                        FGE1/0/49  FGE1/0/50  FGE1/0/51
                                           FGE1/0/52  XGE1/0/1  XGE1/0/2
                                           XGE1/0/3  XGE1/0/4  XGE1/0/5
                                           XGE1/0/6  XGE1/0/7  XGE1/0/8
                                           XGE1/0/9  XGE1/0/10  XGE1/0/11
                                           XGE1/0/12  XGE1/0/13  XGE1/0/14
                                           XGE1/0/15  XGE1/0/16  XGE1/0/17
                                           XGE1/0/18  XGE1/0/19  XGE1/0/20
                                           XGE1/0/21  XGE1/0/22  XGE1/0/23
                                           XGE1/0/24  XGE1/0/25  XGE1/0/26
                                           XGE1/0/27  XGE1/0/28  XGE1/0/29
                                           XGE1/0/30  XGE1/0/31  XGE1/0/32
                                           XGE1/0/33  XGE1/0/34  XGE1/0/35
                                           XGE1/0/36  XGE1/0/37  XGE1/0/38
                                           XGE1/0/39  XGE1/0/40  XGE1/0/41
                                           XGE1/0/42  XGE1/0/43  XGE1/0/44
                                           XGE1/0/45  XGE1/0/46  XGE1/0/47
                                           XGE1/0/48
5         DoesntBelong'''


# Run the text through the FSM.
# The argument 'template' is a file handle and 'raw_text_data' is a
# string with the content from the show_inventory.txt file
template = open("./templates/displayospf.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(raw_text_data)



print (json.dumps(fsm_results, indent=4))

