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
   limitations under the License.
'''
import jtextfsm as textfsm
import json
import os



displayarp = '''<5900>dis arp
  Type: S-Static   D-Dynamic   O-Openflow   R-Rule   M-Multiport  I-Invalid
IP address      MAC address    VLAN     Interface                Aging Type
10.20.10.1      001e-c1dc-fc01 N/A      M-GE0/0/0                16    D
10.20.1.254     001e-c1dc-fc01 1        XGE1/0/47                16    D
10.20.1.2       2c23-3a40-7e18 1        XGE1/0/48                5     D
<5900>'''


displayarpCW5 = '''<HP_5500EI>dis arp
      Type: S-Static    D-Dynamic    O-Openflow
IP Address       MAC Address     VLAN ID  Interface              Aging Type
10.101.0.7       c434-6bb9-ddd8  1        GE1/0/5                19    D
10.101.0.101     0050-5666-7d73  1        GE1/0/5                5     D
10.101.0.20      0050-56b5-7f66  1        GE1/0/6                20    D
10.101.0.202     0050-56b5-df94  1        GE1/0/6                20    D
10.101.0.203     0050-56bb-2aa4  1        GE1/0/6                20    D
10.101.0.6       c434-6bb9-4fbc  1        GE1/0/6                17    D
10.101.0.207     000c-296a-7a91  1        GE1/0/6                7     D
10.101.0.206     000c-290d-1439  1        GE1/0/6                15    D
10.101.0.114     0050-5664-8edb  1        GE1/0/6                14    D
10.101.0.5       000c-2914-5a97  1        GE1/0/6                17    D
10.101.0.31      000a-9c51-33a8  1        GE1/0/10               6     D
10.101.0.32      000a-9c51-46c3  1        GE1/0/11               16    D
10.10.10.30      001b-5354-bf42  10       GE1/0/12               20    D
10.101.0.235     000b-866d-1b88  1        GE1/0/18               20    D
10.101.0.159     1040-f3ee-f0be  1        GE1/0/18               19    D
10.20.10.10      d07e-28ec-aa4c  N/A      GE1/0/22               7     D
10.10.3.5        d07e-2880-400f  3        GE1/0/23               20    D
10.101.0.1       001b-d447-1e68  1        GE1/0/23               19    D
10.101.0.108     7848-5949-1640  1        GE1/0/23               20    D
10.101.0.110     2c41-387f-a8eb  1        GE1/0/23               19    D
10.101.0.105     7848-5949-18c0  1        GE1/0/23               20    D
10.101.15.1      001b-d447-1e68  15       GE1/0/23               20    D
10.101.0.130     c0cb-3863-42cd  1        GE1/0/23               9     D
10.101.0.227     001a-c1f0-1e32  1        GE1/0/23               20    D
10.10.10.5       d07e-2880-400c  10       GE1/0/23               20    D
10.101.0.111     b034-953f-3c01  1        GE1/0/23               3     D
10.10.3.3        d07e-2880-400c  3        GE1/0/23               20    D
10.101.0.125     4001-c613-c1d4  1        GE1/0/23               20    D
10.101.0.126     4001-c613-c1c2  1        GE1/0/23               20    D
10.101.0.41      3c4a-925b-c243  1        GE1/0/23               5     D
10.101.0.231     d07e-2880-400f  1        GE1/0/23               20    D
10.101.0.236     000b-86dc-8e60  1        GE2/0/9                N/A   D
10.101.0.239     0026-8879-a07f  1        GE2/0/13               N/A   D
10.20.1.1        d07e-28ec-aa52  N/A      GE2/0/23               N/A   D
10.20.1.2        2c23-3a40-7e18  N/A      GE2/0/23               N/A   D
10.15.1.1        3c8a-b05d-7b98  N/A      GE2/0/24               N/A   D
<HP_5500EI>'''


template = open("./templates/displayarp.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displayarpCW5)

for i in fsm_results:


for i in fsm_results:
    print (i)