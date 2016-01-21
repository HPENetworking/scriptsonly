# This script is provided with no support or guarantees.
# You may use it, modify and distribute with no restrictions
# as long as original author is mentioned.
#
# Script is designed for embedded operation within Comware OS.
# It purpose is to generate random static routes for lab purposes
# Please note this is not efficient way to do route table size testing,
# for that it is suggested to use other tools that inject routes
# via routing protocol. Usage is limited for lab environment and trainings.
#
# Usage:
# <Switch1>python routegen.py -c 200 -g NULL0
# where -c defines number of random routes and -g gateway (nexthop)
#
# Author: Tomas Kubica
# Contact: tomas.kubica@hp.com

import comware, sys, getopt, random

def main(argv):
    count = 0
    gateway = 'NULL0'
    if len(sys.argv) < 2:
        print 'routegen.py -c <count> -g <gateway>'
        sys.exit()            
    try:
        opts, args = getopt.getopt(argv,"hc:g:",["count=","gateway="])
    except getopt.GetoptError:
        print 'routegen.py -c <count> -g <gateway>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'routegen.py -c <count> -g <gateway>'
            sys.exit()
        elif opt in ("-c", "--count"):
            try:
                count = int(arg)
            except ValueError:
                print 'Count needs to be a number'
                sys.exit()
        elif opt in ("-g", "--gateway"):
            gateway = arg
    
    routestatic = 'ip route-static {0} 32 NULL0'
    command = 'system-view ; '
    print 'Generating routes'
    for i in range(count):
        n1 = str(10)
        n2 = str(random.randrange(1, 254, 1))
        n3 = str(random.randrange(1, 254, 1))
        n4 = str(random.randrange(1, 254, 1))
        ip = n1 + '.' + n2 + '.' + n3 + '.' + n4
        command = command + routestatic.format(ip) + ' ; '
    
    print 'Installing routes'
    comware.CLI(command, False)

if __name__ == "__main__":
   main(sys.argv[1:])
