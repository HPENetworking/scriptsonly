__author__ = 'Dobias van Ingen'


import paramiko
import sys
import os
import time

test = os.system('ping 192.168.56.102')

cmd = "display version\n"
host = '192.168.56.102'
user = 'dobias'
passwd = 'HPRocks2'
port = 22

ip = sys.argv[1]


def etss_range(etssrange):
    hosts = []
    block = etssrange.split('.')
    for x, y in enumerate(block):
        if '-' in y:
            blockrange = y.split('-')
            for z in range(int(blockrange[0]), int(blockrange[1])+1):
                ipaddr = '.'.join(block[:x] + [str(z)] + block[x+1:])
                hosts += etss_range(ipaddr)
            break
    else:
        hosts.append(etssrange)
    return hosts



def main():
    target_ip = etss_range(ip)
    for i in target_ip:
        try:
            t = paramiko.Transport((i, port))
            t.connect(username=user, password=passwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            #Download files
            filepath = '/scripts/test.txt'
            localpath = 'test.txt'
            #dirlist = scp.listdir(filepath)
            #print dirlist
            #sftp.get(filepath, localpath)
            #Upload files
            sftp.put(localpath, filepath)
            time.sleep(15)
            print "SFTP connection established to %s" % (i)
            print "File(s) being uploaded ..."
        except:
            sftp.close()
            t.close()
            print "Problem connecting with ip: %s" % (i)
            continue

if __name__ == "__main__":
    main()

