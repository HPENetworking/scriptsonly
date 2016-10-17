#Meridian ClearPass integration - Agenda use case

Here you can find python script, java script and html files which goal is to:
* Create guests in ClearPass guest
* Associate an agenda to these guest
* Authenticate the guest in Meridian App and get the custom agenda associated to this guest (using Meridian - ClearPass oAuth2 integration)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites : 

* Have a ClearPass installation configured to authenticate Meridian App user through a service in ClearPass
* Have a Meridian App (configured to authenticate through ClearPass)
* Have a MariaDB server (should work with standard MySQL). Please check in the script the DB name and tables used (can be customized).
* Have Apache installed on the server (in my test I used the same server for Apache and MariaDB, which is a Centos Linux)
* Have Python 3.x installed on the server (tested with python 3.4). This will not work with Python 2.x
* Following Python modules must be added (I think the other ones I use are installed by default):
  * cgi and cgitb: can be installed with "pip install cgi cgitb"
  * json: can be installed with "pip install json"
  * request: can be installed with "pip install request"
  * smtplib and email: can be installed with "pip install smtplib email"
  * mysql (I use mysql.connector library to update db): for this one I didn't succeed in installing with pip. So if you also face some issue, please refer to [this doc](http://dev.mysql.com/doc/connector-python/en/) and [this download page](https://dev.mysql.com/downloads/connector/python/)
* Optionnaly : added an AD as an authentication source (in order to be able to use corporate account in the Meridian App)
* Optionnaly : have a yammer developper token (useful if the corporate users are in a Yammer group)

### Description of the main scripts:

* cgi-bin/auth_v2.py: script used to authenticate a Guest Manager for Guest creation / agenda creation (used in index.html page through javascript dynamicform.js)
* cgi-bin/create_client_v2.py: script to create agenda, agenda entries, customer and associate the new agenda to new customers (and eventually corporate user). This script uses mainly mysql.connector function to update the DB and API requests library to create the guest in ClearPass
* cgi-bin/agenda_v2.py: used to display custom agenda for Meridian App (when authenticated). This script get the auth token associated to the Meridian App user (from the headers of the html request), then get parameters associated to the user in ClearPass via API requests, then get agenda data from the Database and finally creates the corresponding html page (using bootstrap, so should display well on any device / window size). This is the page to add 'as an hosted page) in the Meridian App
* cgi-bin/api/UpdateDBwithYammer_V0_2.py: this script is used to update the employee DB with picture URL of the corporate users (using Yammer API). This needs to have a Yammer api token.
* html/index.html: page to create the guests / create the agenda. In this page we have both the authentication and the creation form (in which we can add fields such as guest or agenda entry dynamically using the js/dynamicForm.js java script). Alsu used bootstrap so should be displayed well on any device / window size
* js/dynamicForm.js : java script used to authenticate the guest manager and also to add dynamically guest and agendaEntries fields.
	
### Installation: 
Copy/Paste everything in /var/www/ directory of your Linux Apache Server and give access to cgi-bin, html and pictures to the Apache web.

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