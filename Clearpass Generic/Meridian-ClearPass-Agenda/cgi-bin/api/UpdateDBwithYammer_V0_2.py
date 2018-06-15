#!/usr/bin/env python3.4
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import re
import json
#import sys,getopt
#from sys import argv
import requests
import mysql.connector as mariadb

# DEBUG flag. Change to 1 to display debug info
global DEBUG 
DEBUG = 0

# Replace parameters between <> with your own values

# Function to search email in Yammer through API and update local DB with MySQL connector
def update_DB_Yammer(email):

	YammerBaseURL="https://www.yammer.com"
	auth_token="<Your_Yammer_API_Token>"
	headers={'Authorization':'Bearer ' + auth_token}

	GetUserByEmailURI="/api/v1/users/by_email.json?email="

	result = ""
	if DEBUG:
		print('<li> Email to search in Yammer: %s' %(email))
		print('<BR>')


	url = YammerBaseURL + GetUserByEmailURI + email
	
	if DEBUG:
		print('<li> Yammer API URL to get the user info: %s' %(url))
		print('<BR>')

	try:
		userInfojson = requests.get(url,headers=headers).json()
	except:
		if DEBUG:
			print('<li>User %s not found (or bad Yammer API token)... Exiting' %(email))
			print('<BR>')
		result = '<br>&nbsp;&nbsp;&nbsp;&nbsp;Warning: User %s not found ... Exiting' % (email)
		return result
		#exit(3)
	userPictureTemp = userInfojson[0]['mugshot_url_template']

	if DEBUG:
		print('<li> URL template for the user picture: %s' %(userPictureTemp))
		print('<BR>')

	userPicture=re.sub('\{width\}x\{height\}\/','',userPictureTemp)

	if DEBUG:
		print('<li> User Picture URL after reformat: %s' %(userPicture))
		print('<BR>')

	MySQLQuery = 'INSERT INTO Employee (Email,PictureURL) VALUES (\"%s\",\"%s\") ON DUPLICATE KEY UPDATE PictureURL=\"%s\"' % (email, userPicture, userPicture)

	if DEBUG:
		print('<li> MySQL query to launch to insert this in the DB: %s' % (MySQLQuery))
		print('<BR>')

	mariadb_connection = mariadb.connect(user='root', password='hpn@HPISC', database='Users')
	cursor = mariadb_connection.cursor()

	try:
    		cursor.execute(MySQLQuery)
	except mariadb.Error as error:
		if DEBUG:
    			print("Error: {}".format(error))
		return error

	mariadb_connection.commit()
	lastID = cursor.lastrowid
	if DEBUG:
		print('<li> The last inserted id was: %d ' % (lastID))
		print('<BR>')

	mariadb_connection.close()
	result = '<br>&nbsp;&nbsp;&nbsp;&nbsp;Success ! The last inserted id was: %d' % (lastID)
	return result

# Main. Exit values:
#	0 : Success
#	1 : Missing Parameters
#	2 : Bad script authentication Token
#	3 : User not found in Yammer or bad Yammer Token
def main():

	# I use a token to put minimum security if called from third party (put your own)
	token_script="<Token_of_your_choice>"
	updateResult = ""
	arguments = cgi.FieldStorage()

	mandatory = ["token","email"]

	print('Content-type: text/html\r\n')
	print('')
	print('Beginning of Execution')
	print('<BR>')

	for param in mandatory:
		if param not in arguments.keys():
			print('Missing parameter %s ... exiting' %(param))
			exit(1)
	if (arguments["token"].value) == token_script :
		print('<li>Authentication successfull')
		print('<BR>')
	else :
		print('Bad authentication token (%s). Permission denied' %(arguments["token"].value))
		exit(2)

	userEmail = arguments["email"].value
	#UserEmail=arguments.getvalue('email') -- Another Way to do it

	updateResult = update_DB_Yammer(userEmail)

	if 'Warning' in updateResult:
		exit(3)
	else:
		exit(0)

# Prevents from running main automatically when importing this file
if __name__ == "__main__":
	main()
