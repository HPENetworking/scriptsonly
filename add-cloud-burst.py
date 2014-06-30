# This script can be used for Virtual Router demonstrations to set-up EVI tunnel
# when needed


__author__ = 'Chuck Dilts'

import comware
import time

comware.CLI('system-view ;evi site-id 1 ; evi designated-vlan 10 ;return ')
time.sleep(1)
comware.CLI('system-view ; interface Tunnel1 mode evi ; evi arp-suppression enable ; evi extend-vlan 10 ; source LoopBack0 ; evi network-id 100 ; evi neighbor-discovery client enable 3.3.3.1 ; return ')
time.sleep(1)
comware.CLI('system-view ; interface GigabitEthernet2/0 ; evi enable ; return ')
print 'EVI has been added'


