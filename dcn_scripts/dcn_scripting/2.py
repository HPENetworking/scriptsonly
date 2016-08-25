#!/usr/bin/env python
'''
 Copyright 2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__copyright__ = "Copyright 2016, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

test connectivity to the VSD API

'''
from vspk import v3_2 as vsdk

# Configuring a connection to the VSD API
nc = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url="https://10.132.0.126:8443")

# Actively connecting ot the VSD API
nc.start()
print ('Auth success')

# Root User
nuage_user = nc.user

domain = nuage_user.domains.get_first(filter='name == "Default Domain"')
doimain.fetch()
print domain.id
#domain.fetch()
domain.name = 'Superx'
ent = nuage_user.enterprises.get_first(filter='name == "Joe"')
#print ('This is the enterprise ') + ent.name
job = vsdk.NUJob(command='EXPORT')

# Creating export job for the Main VSPK Domain

domain.create_child(job)

# Printing the export result

while True:
    job.fetch()
    if job.status == 'SUCCESS':
        # Using the export copy of the domain details from above
        import_job = vsdk.NUJob(command='IMPORT', parameters=job.result)
        ent.create_child(import_job)
        break

    if job.status == 'FAILED':
        pass
    time.sleep(1)

#ent.create_child(domain)
