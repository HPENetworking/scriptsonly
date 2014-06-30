# This script can be used for Virtual Router demonstrations to remove EVI tunnel
# when no longer needed


__author__ = 'Chuck Dilts'

import comware


comware.CLI('system-view ; undo int tun 1 ; undo evi site-id ; undo evi designated-vlan ; return ')
comware.CLI('system-view ; interface GigabitEthernet2/0 ; undo evi enable ; return ')
print 'EVI has been removed' 




