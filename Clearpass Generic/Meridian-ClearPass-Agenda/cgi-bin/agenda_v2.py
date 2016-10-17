#!/usr/bin/env python3.4
'''
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


__author__ = "@netmanfabe"
__copyright__ = "Copyright 2016, Hewlett Packard Enterprise Development LP."
__credits__ = ["Fabien GIRAUD"]
__license__ = "Apache2"
__version__ = "2.0.0"
__maintainer__ = "Fabien GIRAUD"
__email__ = "fabien_giraud@me.com"
__status__ = "Prototype"

'''

# This script is the one called in the Meridian App Agenda Web page in order to get agenda entries associated to the 
# connected user, and generate a web page corresponding to this agenda

import json
import sys
import mysql.connector as mariadb
import requests
import cgi
import cgitb; cgitb.enable() # Optional: for debugging only
import re

# Global parameters
# Replace the parameters between <> with yours
global CPPMBaseURL
CPPMBaseURL = "https://<your_CPPM_url>"

# Default values for DB connection
global DBUser
global DBPassword
global DBName
DBUser = '<Your_DB_User>'
DBPassword = '<Your_DB_Password>'
DBName = '<YOUR_DB_NAME In my setup I used db name : Users>'	# This is the name of the DB I use to publish the info. You can change it with your own


def html_header():
	print("""Content-type:text/html ; charset=utf-8\n\n
		<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="utf-8"/>
					<title>Login Form</title>
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
				</head>
				<body>""")
	print("""
				<div class="container-fluid">""")

def html_footer():
	print("""
				</div>
					<script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
					<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
					<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
				</body>
			</html>""")


def error(name, description):
	html_header()
	print("<h2>%s</h2>" % name)
	print(description)

# Function to load the agenda: with the token present in the header, it gets the agenda id and then constructs the agenda based on DB queries
# Argument : token
def load_agenda(token):

	meURI = "/api/oauth/me"
	headers={'Authorization':'Bearer ' + token ,'Content-Type':'application/json'}

	url = CPPMBaseURL + meURI
	# API URI call to get ClearPass user specific attribute based on the token parameter
	data = requests.post(url,headers=headers).json()


	if 'status' in data:
		error('Guest Error', 'Can\'t fetch guest informations.\nThe session may be expired (status %s)' % data['status'])
		return 
	if 'agenda' not in data:
		error('No agenda', 'Guest is not associated with any agenda')
	
	# Print the name of the user based on parameter got from CPPM
	print("""
				<div class="page-header text-center">
					<div class="row">
						<div class="col-xs-8 col-sm-8 col-md-11 col-lg-11">
							<BR><h3>Agenda for %s</h3>
				""" %(data['name']))


	
	dateFormat = '%m/%d/%Y'
	# SQL query to retrieve Agenda main info (based on User CPPM parameter : Agenda
	agendaSQLQuery = 'select Title,Location,Logo,DATE_FORMAT(Date,\'%s\') from Agenda where ID = %s' %(dateFormat,data['agenda'])

	SQLResult = get_db_query(agendaSQLQuery)

	size = '100'
	#print (SQLResult)	
	# Displaying this in the heml page
	for (Title,Location,Logo,Date) in SQLResult:
		if data['image']:
			print("""
					 		<h4>%s, Date: %s</h4>
						</div>
						<div class="col-xs-4 col-sm-4 col-md-1 col-lg-1">
							<BR>
							<img class="img-responsive" src="%s" alt="%s">
						</div>
					</div>
				</div>""" %(Title,Date,data['image'],data['badge']))
		elif Logo:
			print("""
					 		<h4>%s, Date: %s</h4>
						</div>
						<div class="col-xs-4 col-sm-4 col-md-1 col-lg-1">
							<BR>
							<img class="img-responsive" src="%s" alt="%s">
						</div>
					</div>
				</div>""" %(Title,Date,Logo,data['badge']))
		else:
			print("""
					 		<h4>%s, Date: %s</h4>
						</div>
						<div class="col-xs-4 col-sm-4 col-md-1 col-lg-1 text-center">
							<BR>
							%s
						</div>
					</div>
				</div>""" %(Title,Date,data['badge']))

	print("""
				<div class="row">
					<div class="col-xs-4 col-sm-3 col-md-2 col-lg-2"><img class="img-responsive" src="/pictures/InnoCenter.png"></div>""")
					
	timeFormat = '%h:%i'
	
	# SQL query to retrieve all the agenda entries corresponding to the agenda (using the agenda ID)
	agendaEntriesSQLQuery = 'select DATE_FORMAT(StartTime,\'%s\'),DATE_FORMAT(EndTime,\'%s\'),Content,Presenter,Day from AgendaEntry where AgendaID = %s order by Day,StartTime;' %(timeFormat,timeFormat,data['agenda'])


	SQLResult = get_db_query(agendaEntriesSQLQuery)

	print("""
					<div class="col-xs-8 col-sm-9 col-md-10 col-lg-10">
						<table class="table table-striped">
						<thead>
							<tr>
								<th COLSPAN=3 class="text-center">Location: %s</th>
							</tr>
							<tr>
								<th class="text-center">When?</th>
								<th class="text-center">What?</th>
								<th class="text-center">Who</th>
							</tr>
						</thead>
				""" %(Location))

	#print (SQLResult)

	print("""				<tbody>""")
	prevDay = -1
	# I select all the fields, including end time but I don't use it to make the table lighter.
	# If needed this can be used
	for (StartTime,EndTime,Content,Presenter,Day) in SQLResult:
		if (Day != 0 and Day != prevDay):
			print("""
							<TR>
								<TD COLSPAN=3 class="text-center">Day %s</TD>
							</TR>""" %(Day))
		prevDay = Day
		#print("Session: %s starts at %s and ends at %s on day %s. Presenter is %s" %(Content,StartTime,EndTime,Day,Presenter))
		print("""
							<TR>
								<TD>%s</TD>
								<TD>%s</TD>
								<TD>%s</TD>
							</TR>""" %(StartTime,Content,Presenter))

	print("""				</tbody>
						</table>
					</div>
				</DIV>
				<div class="row">
					<div class="col-xs-4 col-sm-4 col-md-2 col-lg-2"><img class="img-responsive" src="/pictures/Hewlett_Packard_Enterprise_logo_svg.png"></div>
					<div class="col-xs-4 col-sm-4 col-md-2 col-lg-2"><img class="img-responsive" src="/pictures/aruba_hpe.svg"></div>
				</DIV>
					
				""")


# Function get_db_query is designed to execute a sql query to get info, such as select, and return these info
# Args : SQLquery, user, password and db name which are default to global parameters
# Return a list where each entry correspond to a lin e the query result
def get_db_query(MySQLQuery,user=DBUser,password=DBPassword,database=DBName):

	mariadb_connection = mariadb.connect(user=user, password=password, database=database)
	cursor = mariadb_connection.cursor()

	cResult = []
	try:
		cursor.execute(MySQLQuery)
	except mariadb.Error as error:
		print("Error: {}".format(error))
		return null

	
	for p in cursor:
		cResult.append(p)

	return cResult

	
def main():

	try:
		import os
		token =re.sub('Bearer ','',os.environ['HTTP_AUTHORIZATION'])

# Since last Meridian update the way we can get the token has changed
#	This is why I commented the below and use now the above line
#		fields = cgi.FieldStorage() 
#		token = cgi.FieldStorage()["token"].value

	except IndexError:
		error('Authorization Error', 'Missing authorization header')

	html_header()
	load_agenda(token)
	html_footer()


# To prevent executed the main if importing this file in another one
if __name__ == "__main__":
	main()
