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

# This script is provided with no support or guarantees.
#
# Purpose of this script is to save configuration to remote FTP server
# File is automatically generate in form of sysname_timestamp.cfg
#
# Usage:
# ftpsave.py -s <serverIP> -u <FTPusername> -p <FTPpassword> -d (to delete file after transfer)
# If you run script without arguments only local file will be created.
#
# You may schedule automatic configuration save by leveraging Comware scheduler:
# [Switch1]scheduler job ftp_archive
# [Switch1-job-ftp_archive]command 0 python cfgsave.py -s 172.16.1.3 -u ftp -p ftp -d
# [Switch1-job-ftp_archive]quit
# [Switch1]scheduler schedule autobackup
# [Switch1-schedule-autobackup]user-role network-admin
# [Switch1-schedule-autobackup]job ftp_archive
# [Switch1-schedule-autobackup]time repeating interval 60
# [Switch1-schedule-autobackup]quit
# [Switch1]
#
# Also you may use EAA to automatically push configuratio to FTP server
# every time administrator enter save command:
# [Switch1]rtm cli-policy ftp_backup
# [Switch1-rtm-ftp_backup]event cli async mode execute pattern save*
# [Switch1-rtm-ftp_backup]action 0 cli python cfgsave.py -s 172.16.1.3 -u ftp –p ftp -d
# [Switch1-rtm-ftp_backup]user-role network-admin
# [Switch1-rtm-ftp_backup]commit
# [Switch1-rtm-ftp_backup]



import comware, sys, getopt, os, datetime, socket

def main(argv):
    ip = ''
    username = ''
    password = ''
    delete = False
    try:
        opts, args = getopt.getopt(argv,"hds:p:u:",["server=","username=","password="])
    except getopt.GetoptError:
        print 'usage ftpsave.py -s <serverIP> -u <FTPusername> -p <FTPpassword> -d (to delete file after transfer)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'usage ftpsave.py -s <serverIP> -u <FTPusername> -p <FTPpassword> -d (to delete file after transfer)'
            sys.exit()
        elif opt in ("-s", "--server"):
            ip = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-d", "--delete"):
            delete = True

    timestamp = datetime.datetime.now().strftime("%y%m%d%H%M")
    sysname = socket.gethostname()
    filename = sysname + '_' + timestamp + '.cfg'
    filenamemdb = sysname + '_' + timestamp + '.mdb'
    comware.CLI('save ' + filename)

    if ip != '':
        path = 'ftp://' + username + ':' + password + '@' + ip + '/'
        comware.CLI('copy ' + filename + ' ' + path)
        if delete: 
            comware.CLI('delete ' + filename)
            comware.CLI('delete ' + filenamemdb)

if __name__ == "__main__":
   main(sys.argv[1:])
