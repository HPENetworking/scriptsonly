''' for python 3 reqires for of textFSM avialable at https://github.com/jonathanslenders/textfsm'''
import jtextfsm as textfsm
import json
import os




#Display Radius Scheme Output from HPE 5500EI Comware 5 Switch

displayradiusschemeCW5 = '''<HP_5500EI>dis radius scheme
------------------------------------------------------------------
SchemeName  : system
  Index : 0                           Type : extended
  Primary Auth Server:
    IP: 127.0.0.1                                Port: 1645   State: active
    Encryption Key : N/A
    VPN instance   : N/A
    Probe username : N/A
    Probe interval : N/A
  Primary Acct Server:
    IP: 127.0.0.1                                Port: 1646   State: active
    Encryption Key : N/A
    VPN instance   : N/A
  Auth Server Encryption Key : N/A
  Acct Server Encryption Key : N/A
  VPN instance               : N/A
  Accounting-On packet disable, send times : 50 , interval : 3s
  Interval for timeout(second)                            : 3
  Retransmission times for timeout                        : 3
  Interval for realtime accounting(minute)                : 12
  Retransmission times of realtime-accounting packet      : 5
  Retransmission times of stop-accounting packet          : 500
  Quiet-interval(min)                                     : 5
  Username format                                         : without-domain
  Data flow unit                                          : Byte
  Packet unit                                             : one


------------------------------------------------------------------
SchemeName  : imcradius
  Index : 1                           Type : extended
  Primary Auth Server:
    IP: 10.3.10.220                              Port: 1812   State: active
    Encryption Key : N/A
    VPN instance   : N/A
    Probe username : N/A
    Probe interval : N/A
  Primary Acct Server:
    IP: 10.3.10.220                              Port: 1813   State: active
    Encryption Key : N/A
    VPN instance   : N/A
  Auth Server Encryption Key : ******
  Acct Server Encryption Key : ******
  VPN instance               : N/A
  Accounting-On packet disable, send times : 50 , interval : 3s
  Interval for timeout(second)                            : 3
  Retransmission times for timeout                        : 3
  Interval for realtime accounting(minute)                : 12
  Retransmission times of realtime-accounting packet      : 5
  Retransmission times of stop-accounting packet          : 500
  Quiet-interval(min)                                     : 5
  Username format                                         : without-domain
  Data flow unit                                          : Byte
  Packet unit                                             : one
  NAS-IP address                                          : 10.10.3.1


------------------------------------------------------------------
SchemeName  : dot1x
  Index : 2                           Type : standard
  Auth Server Encryption Key : N/A
  Acct Server Encryption Key : N/A
  VPN instance               : N/A
  Accounting-On packet disable, send times : 50 , interval : 3s
  Interval for timeout(second)                            : 3
  Retransmission times for timeout                        : 3
  Interval for realtime accounting(minute)                : 12
  Retransmission times of realtime-accounting packet      : 5
  Retransmission times of stop-accounting packet          : 500
  Quiet-interval(min)                                     : 5
  Username format                                         : with-domain
  Data flow unit                                          : Byte
  Packet unit                                             : one


------------------------------------------------------------------
Total 3 RADIUS scheme(s).

<HP_5500EI>'''

#Display Radius Scheme Output from HPE 5900 Comware 7 Switch

displayradiusschemeCW7 = '''5900>display radius scheme
Total 1 RADIUS schemes

------------------------------------------------------------------
RADIUS scheme name: system
  Index: 0
  Primary Auth Server:
    Host name: Not Configured
    IP  : Not Configured                           Port: 1812   State: Block
    VPN : Not configured
  Primary Acct Server:
    Host name: Not Configured
    IP  : Not Configured                           Port: 1813   State: Block
    VPN : Not configured

  Accounting-On function                     : Disabled
    Retransmission times                     : 50
    Retransmission interval(seconds)         : 3
  Timeout Interval(seconds)                  : 3
  Retransmission Times                       : 3
  Retransmission Times for Accounting Update : 5
  Server Quiet Period(minutes)               : 5
  Realtime Accounting Interval(minutes)      : 12
  NAS IP Address                             : Not configured
  VPN                                        : Not configured
  User Name Format                           : Without-domain
  Data flow unit                             : Byte
  Packet unit                                : One
  Attribute 15 check-mode                    : Strict
------------------------------------------------------------------
<5900>'''

template = open("./templates/displayradiusschemeCW7.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(displayradiusschemeCW7)

print (fsm_results)