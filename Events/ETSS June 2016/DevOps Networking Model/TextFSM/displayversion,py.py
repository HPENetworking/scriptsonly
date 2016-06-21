''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
import jtextfsm as textfsm
import json
import os



displayversion = """<5900>dis version
HP Comware Software, Version 7.1.045, Release 2418P06
Copyright (c) 2010-2015 Hewlett-Packard Development Company, L.P.
HP 5900AF-48XGT-4QSFP+ Switch uptime is 1 week, 0 days, 19 hours, 33 minutes
Last reboot reason : Cold reboot

Boot image: flash:/5900_5920-cmw710-boot-r2418p06.bin
Boot image version: 7.1.045, Release 2418P06
  Compiled Aug 07 2015 15:40:53
System image: flash:/5900_5920-cmw710-system-r2418p06.bin
System image version: 7.1.045, Release 2418P06
  Compiled Aug 07 2015 15:40:53


Slot 1:
Uptime is 1 week,0 days,19 hours,33 minutes
5900AF-48XGT-4QSFP+ Switch with 2 Processors
BOARD TYPE:         5900AF-48XGT-4QSFP+ Switch
DRAM:               2048M bytes
FLASH:              512M bytes
PCB 1 Version:      VER.B
Bootrom Version:    142
CPLD 1 Version:     004
CPLD 2 Version:     004
Release Version:    HP 5900AF-48XGT-4QSFP+ Switch-2418P06
Patch Version  :    None
Reboot Cause  :     ColdReboot
[SubSlot 0] 48XGT+4QSFP Plus
<5900>"""

template = open("./templates/displayversion.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displayversion)

for i in fsm_results:
    print (i)