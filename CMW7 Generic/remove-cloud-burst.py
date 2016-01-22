# This script can be used for Virtual Router demonstrations to remove EVI tunnel
# when no longer needed

''' Copyright 2016 Hewlett Packard Enterprise Development LP.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.'''


__author__ = 'Chuck Dilts'

import comware


comware.CLI('system-view ; undo int tun 1 ; undo evi site-id ; undo evi designated-vlan ; return ')
comware.CLI('system-view ; interface GigabitEthernet2/0 ; undo evi enable ; return ')
print 'EVI has been removed' 




