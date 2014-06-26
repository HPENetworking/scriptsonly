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