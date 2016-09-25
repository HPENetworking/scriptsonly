#UpdateDBWith Yammer

Here you can find a script which allow to get user info (in this example picture url) using his email from a Yammer group.
It is based on Yammer API. The information is stored in a MariaDB database and the aim of the script is to be used in a ClearPass Context Server Action (so the info can be added / updated when a user connect via ClearPass).

Prerequisite : have a MariaDB server. Please check in the script the DB name and tables used.



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