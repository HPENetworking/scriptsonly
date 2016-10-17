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

# In this script, based on the data in the index.html form, we create the agenda and agenda entries in the DB,
# then we create the guests in the DB and ClearPass, and finally associates the guest and employees to the agenda (using Agenda ID)

import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import json
import datetime
import mysql.connector as mariadb
from api import UpdateDBwithYammer_V0_2 as upYam
import requests
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders

# Global Variables
# Change the parameters between <> to match you environment
# If DB is another server you need to change the connection query (in the function execute_db_query)
global CPPMBaseURL
global DBUser
global DBPassword
global DBName
global fromAddr
global SMTPServ
CPPMBaseURL = "https://<Your_CPPM_URL>"
DBUser = '<YOUR_DB_USER>'
DBPassword = '<YOUR_DB_PASSWORD>'
DBName = '<YOUR_DB_NAME In my setup I used db name : Users>'
fromAddr = '<your_from_email_address>'	# Email address from which an email will be sent to corporate users. For guest this is down directly by ClearPass
SMTPServ = '<Your_SMTP_Server>'


# Function randomPassword generate string
# Parameters: 	size = the size of the desired password (default 6)
#		chars = set of characters to be used (default Upper case letters + digits)
def randomPassword(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# This function create_each_customer creates each customer using CPPM API calls and MySQL connector for local DB
# First release was using external call for API. Now we do everything with request library
# Arguments are: CPPM token, a dictionnary based on filtered cgi FormFields
# It also use global var agendID for the localDB update
def create_each_customer(token, data):

# First we create the guest in CPPM

	headers={'Authorization':'Bearer ' + token ,'Content-Type':'application/json'}
	BaseURI ="/api/guest"

	# Try to create the guest

	CreateURI = BaseURI
	url = CPPMBaseURL + BaseURI

	try:
		# API request for guest creation
		apiResult = requests.post(url,headers=headers,data=json.dumps(data)).json()
	except:
		out = 'Warning: User can\'t be updated: ' + data['username']
	
	if ('status' in apiResult):
	# This means the user already exists --> update (PATCH) it		

	# First get user id 
	# (finally use another method directly with username see below)
#		GetUserURI=BaseURI + "/api/guest/username/" + data['username']
#		url = CPPMBaseURL + GetUserURI 
#
#		try:
#			userInfojson = requests.get(url,headers=headers).json()
#		except:
#			out = 'Warning: User not found for update: ' + data['username'] + '!!'
#		userID = userInfojson['id']

		# API request for guest update (directly using his username, no need to find the id first)
		PatchUserURI =BaseURI + "/username/" + data['username']
		url = CPPMBaseURL + PatchUserURI
		
		try:
			apiResult = requests.patch(url,headers=headers,data=json.dumps(data)).json()
		except:
			out = 'Warning: User can\'t be updated: ' + data['username']
		if ('status' in apiResult):
			out = 'Warning: We encountered an issue when updating account ' + data['username'] + 'Status CODE : ' + str(apiResult['status'])
		else:
			out = 'Success: Account updated successfully ' + data['username'] 
			
	else:
	# USer well created
		out = 'Success'

# Second STEP : we now create the guest in the DB and link it to the agenda ID

	MySQLQuery = 'INSERT INTO Guest (Name,Email,AgendaID,PictureURL,Company) VALUES (\"%s\",\"%s\",\"%d\",\"%s\",\"%s\") ON DUPLICATE KEY UPDATE Name=\"%s\", AgendaID=\"%d\", PictureURL=\"%s\", Company=\"%s\"' % (data['visitor_name'],data['email'],agendaID,data['visitor_picture'],data['visitor_company'],data['visitor_name'],agendaID,data['visitor_picture'],data['visitor_company'])

	lastID = execute_db_query(MySQLQuery)

	if (not lastID):
	# Insertion error
		result = "Warning: Cannot update customer "+ data['email'] +" in local DB. Please Check with DB admin"
		# We exit the function
		return result
	else:
	# Everything OK
		result = "Customer " + data['email'] + " created or updated successfully in local DB"

	out += '<BR>&nbsp;&nbsp;&nbsp;&nbsp;' + result
	return out


# This function create_customers will creates all the customers entries in both CPPM Guest DB and also local MariaDB
# It takes the cgi formfields as arguments
# For each customer, this calls create_each_customer function for each customer
def create_customers(args):

	visitor_name = {}
	visitor_company = {}
	email = {}
	visitor_picture = {}
	creationResult = ""

	clientArgs = ["visitor_name", "visitor_company", "email" , "visitor_picture"]

	for p in args.keys():
		if any(s in p for s in clientArgs):
			tmpVal = args[p].value
			tmpSplit = p.split('-')
			if tmpSplit[0] == "visitor_name":
				visitor_name[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "visitor_company":
				 visitor_company[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "email":
				 email[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "visitor_picture":
				 visitor_picture[tmpSplit[1]] = tmpVal

			
	first = 1
	d = {}
	
	# Here you can customize with your own values
	# 	- source: the guestUser:source in ClearPass Guest
	#	- essid : the SSID for visitors wifi so the customer can use same cred for Meridian App and guest Wifi
	#	- ...
	fixed = {"enabled": True, "expire_time": 1483896004, "role_id": 2, "source": "hpe-aruba-guestRegister", "auto_send_smtp": 1, "essid": "Aruba-Guest" }

	token = args['token'].value
	for i in email.keys() :
		d['visitor_name'] = visitor_name[i]
		d['visitor_company'] = visitor_company[i]
		d['email'] = email[i]
		d['visitor_picture'] = visitor_picture[i]

		d['password'] = randomPassword()
		d['username'] = d['email']
		dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		d['start_tume'] = dt
		d['visitor_agenda'] = agendaID

		for p in fixed:
			d[p] = fixed[p]

		if first:
			creationResult = create_each_customer(token, d)
			first = 0
		else:
			creationResult += '<BR>' + create_each_customer(token, d)
	return creationResult

#This function create_each_employee creates/updates (as the name says) each employee in local DB
# Argument is Employee email and it uses also global var agendaID
def create_each_employee(employee):

# Here we don't need to create the guest in CPPM, since CPPM get the info directly in the AD
# So only one step : create / update in the DB (and send an email)
	result=""
	MySQLQuery = 'INSERT INTO Employee (Email,AgendaID) VALUES (\"%s\",\"%d\") ON DUPLICATE KEY UPDATE AgendaID=\"%d\"' % (employee,agendaID,agendaID)
	lastID = execute_db_query(MySQLQuery)

	#PArameters to send an email
	msg = MIMEMultipart('alternative')
 
	msg['Subject'] = "HPE Innovation Center Workshop new Agenda"
	msg['From'] = fromAddr
	msg['To'] = employee

	# text will be used if html can't be read
	text = "A new agenda was associated to your Innovation Center meridian account\nYou can see it by opening the following url https://is.gd/qzvfQl (after having installed the Meridian AppViewer app)"

	html = """\
		<html>
			<head>
			<H1>A new Innovation Center Workshop agenda was associated to your corporate account</H1>
			</head>
			<BODY>

	
			<table width="100%" cellpadding="0" cellspacing="0" border="0">

				<tr>
				<td valign="top">
					<h3 style="font-size:20px;line-height:20px;font-weight:bold;margin:0 0 10px 0;padding:0;">
					Meridian App Instructions:
				</h3>
					<ul style="list-style-type:none;list-style-position:inside;margin:0;padding:0;">
						<li>
							Download and install AppViewer for IOS or Android: <a href="http://getappviewer.com">http://getappviewer.com</a>
						</li>
						<li>
							From your smartphone, browse to the following url:<br> <a href="https://is.gd/qzvfQl">https://is.gd/qzvfQl</a>
						</li>
					
						<li>
							<i>(Optionally)</i>: Login into the app (Top right menu on Android, and bottom right <i>Account</i> link on iOS)with your corporate email / password.

						</li>

					</ul>
				</td>
			</tr>
		</table>
		</BODY>
	</HTML>
	"""

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP(SMTPServ)
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(fromAddr, employee, msg.as_string())
	s.quit()

	result = upYam.update_DB_Yammer(employee) + '(for Yammer Info)'
 
	if (not lastID):
	# Insertion error
		result += "<BR>Warning: Cannot update employee "+ employee +" in local DB. Please Check with DB admin" + '(for AgendaID)'
		# We exit the function
		return result
	else:
	# Everything OK
		result += "<BR>Employee " + employee + " created or updated successfully in local DB" + '(for AgendaID)'

	return result

# This function create_employees will create/update employees in local DB
# Argument is field form corpEmails
def create_employees(Employees):
	listEmployees = Employees.split(',')
	creationResult = ""
	for e in listEmployees:
		creationResult += '<BR>' + create_each_employee(e)
	return creationResult
		

# This function will create each agenda entry in corresponding db
# Takes dictionnary based on filtered cgi FormFields as argument
def create_agenda_entry(data):

#	MySQLQuery = 'INSERT INTO AgendaEntry (AgendaID,StartTime,EndTime,Content,Presenter,Day) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (agendaID,data['begin'],data['end'],data['content'],data['pres'],data['day'])
	MySQLQuery = 'INSERT INTO AgendaEntry (AgendaID,StartTime,Content,Presenter,Day) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (agendaID,data['begin'],data['content'],data['pres'],data['day'])


	lastID = execute_db_query(MySQLQuery)

	if (not lastID):
	# Insertion error
		result = "Warning: Cannot add agenda entry (begin time "+ data['begin'] +" in local DB. Please Check with DB admin"
		# We exit the function
		return result
	else:
	# Everything OK
		result = "Entry at " + data['begin'] + " created successfully in local DB"
	return result

# This function create_agenda will create first the agenda (Title, Location and Date) in corresponding table.
# Arguments for this function are the cgi formfields
# Then it calls the create_agenda_entry function for each agenda entry of the form
def create_agenda(args):
	
	title = args['title'].value
	location = args['location'].value
	date = args['date'].value
	logo = args['logo'].value
	dateFormat = '%m/%d/%Y'

	creationResult = ""

	# SQL query to add an angenda in table agenda
	MySQLQuery = 'INSERT INTO Agenda (Title,Location,Date,Logo) VALUES (\"%s\",\"%s\",STR_TO_DATE(\"%s\",\"%s\"),\"%s\")' %(title,location,date,dateFormat,logo)

#	print('<li> MySQL query to launch to insert this in the DB: %s' % (MySQLQuery))
#	print('<BR>')

	# We save the agenda ID as a global variable to reuse it in Guest and Employee creation
	global agendaID
	agendaID = execute_db_query(MySQLQuery)

	if (not agendaID):
	# Insertion error
		creationResult = "Warning: Cannot create Agenda "+ title +". Please Check logs !"
		# We exit the function
		return creationResult
	else:
	# Everything OK
		creationResult = "Agenda " + title + " created successfully"

	# Now let's create all the agenda entries
	# If you want also to use end time, just uncomment

	begin = {}
#	end = {}
	content = {}
	pres = {}
	day = {}

#	entryArgs = ["begin","end","content","pres","day"]
	entryArgs = ["begin","content","pres","day"]

	for p in args.keys():
		if any(s in p for s in entryArgs):
			tmpVal = args[p].value
			tmpSplit = p.split('-')
			if tmpSplit[0] == "begin":
				begin[tmpSplit[1]] = tmpVal
#			elif tmpSplit[0] == "end":
#				end[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "content":
				content[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "pres":
				pres[tmpSplit[1]] = tmpVal
			elif tmpSplit[0] == "day":
				day[tmpSplit[1]] = tmpVal
	
	d = {}

	for i in begin.keys():
		d['begin'] = begin[i]
#		d['end'] = end[i]
		d['content'] = content[i]
		d['pres'] = pres[i]
		d['day'] = day[i]
		
		creationResult += '<BR>&nbsp;&nbsp;&nbsp;&nbsp;' + create_agenda_entry(d)
	return creationResult

def execute_db_query(SQLQuery,user=DBUser,password=DBPassword,database=DBName):
	
	mariadb_connection = mariadb.connect(user=user, password=password, database=database)
	cursor = mariadb_connection.cursor()

	try:
    		cursor.execute(SQLQuery)
	except mariadb.Error as error:
#		print("Error: {}".format(error))
		return 1

	mariadb_connection.commit()
#	print('<li> The last inserted id was: %s' % (cursor.lastrowid))
#	print('<BR>')
	
	lastInsertedID = cursor.lastrowid

	mariadb_connection.close()

	return lastInsertedID


# Main

def main():

	print('Content-type: application/json')
	print('')
	cgiArgs = cgi.FieldStorage()
	corpEmails = cgiArgs['corpEmails'].value

	result = create_agenda(cgiArgs)
	result += "<BR>" + create_customers(cgiArgs)

	if corpEmails:
		result += create_employees(corpEmails)

	if ('Warning' in result):
		displayMessage = result.replace("Success,","")
		print('{"response": {"result": {"message" : "' + displayMessage + 'User(s) not listed successfully added"}}}')
	else:
		print('{"response": {"Status": "OK"}}')


# To prevent executed the main if importing this file in another one
if __name__ == "__main__":
	main()
