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




displaystp = '''<5900>display stp
-------[CIST Global Info][Mode MSTP]-------
 Bridge ID           : 32768.d07e-28ec-aa48
 Bridge times        : Hello 2s MaxAge 20s FwdDelay 15s MaxHops 20
 Root ID/ERPC        : 32768.d07e-28ec-aa48, 0
 RegRoot ID/IRPC     : 32768.d07e-28ec-aa48, 0
 RootPort ID         : 0.0
 BPDU-Protection     : Disabled
 Bridge Config-
 Digest-Snooping     : Disabled
 TC or TCN received  : 0
 Time since last TC  : 0 days 21h:14m:54s

----[Port49(FortyGigE1/0/49)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.49
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.49
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port50(FortyGigE1/0/50)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.50
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.50
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port51(FortyGigE1/0/51)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.51
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.51
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port52(FortyGigE1/0/52)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.52
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.52
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port1(Ten-GigabitEthernet1/0/1)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.1
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.1
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port2(Ten-GigabitEthernet1/0/2)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.2
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.2
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0

----[Port3(Ten-GigabitEthernet1/0/3)][DOWN]----
 Port protocol       : Enabled
 Port role           : Disabled Port
 Port ID             : 128.3
 Port cost(Legacy)   : Config=auto, Active=200000
 Desg.bridge/port    : 32768.d07e-28ec-aa48, 128.3
 Port edged          : Config=disabled, Active=disabled
 Point-to-Point      : Config=auto, Active=false
 Transmit limit      : 10 packets/hello-time
 TC-Restriction      : Disabled
 Role-Restriction    : Disabled
 Protection type     : Config=none, Active=none
 MST BPDU format     : Config=auto, Active=802.1s
 Port Config-
 Digest-Snooping     : Disabled
 Rapid transition    : False
 Num of VLANs mapped : 1
 Port times          : Hello 2s MaxAge 20s FwdDelay 15s MsgAge 0s RemHops 20
 BPDU sent           : 0
          TCN: 0, Config: 0, RST: 0, MST: 0
 BPDU received       : 0
          TCN: 0, Config: 0, RST: 0, MST: 0'''


template = open("./templates/displaystp.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displaystp)

for i in fsm_results:
    print (i)