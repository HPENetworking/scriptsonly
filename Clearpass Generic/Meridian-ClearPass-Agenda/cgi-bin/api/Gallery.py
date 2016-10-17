#!/usr/bin/env python

# Display all the picture stored in employee table
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
import mysql.connector as mariadb

print('Content-type: text/html\r\n')

MySQLQuery = 'select Email,PictureURL from Employee'

mariadb_connection = mariadb.connect(user='root', password='hpn@HPISC', database='Users')
cursor = mariadb_connection.cursor()

try:
    cursor.execute(MySQLQuery)
except mariadb.Error as error:
    print("Error: {}".format(error))

for (Email,PictureURL) in cursor:
	if (PictureURL  and ('no_photo' not in PictureURL)):
		print("<img src=\"{}\" style=\"width:192px;\">".format(PictureURL))
	else:
		print("<BR>%s does not have any picture in Yammer (or account does not exist)!" % (Email))
#	print("<img src=\"{}\" alt=\"{}\" style=\"width:192px;\" title=\"{}\">".format(PictureURL,Email,Email))
#	print("<img src=\"{}\" alt=\"{}\" style=\"width:96px;height:96px;\">".format(PictureURL,Email))

cursor.close()
mariadb_connection.close()

