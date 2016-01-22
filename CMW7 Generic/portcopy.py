# This script is provided with no support or guarantees.
# You may use it, modify and distribute with no restrictions
# as long as original author is mentioned.
#
# Script is designed for embedded operation within Comware OS.
# It purpose is to copy full configuration of one to another port
#
# Usage:
# <Switch1>python portcopy.py -s g1/0/2 -d g1/0/5
# where -s is source port and -d destination port
#
# Author: Tomas Kubica
# Contact: tomas.kubica@hp.com

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



import comware, sys, getopt

def main(argv):
    sourceport = ''
    destinationport = ''
    if len(sys.argv) < 2:
        print 'portcopy.py -s <sourceport> -d <destinationport>'
        sys.exit()            
    try:
        opts, args = getopt.getopt(argv,"hs:d:",["source=","destination="])
    except getopt.GetoptError:
        print 'portcopy.py -s <sourceport> -d <destinationport>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'portcopy.py -s <sourceport> -d <destinationport>'
            sys.exit()
        elif opt in ("-s", "--source"):
            sourceport = arg
        elif opt in ("-d", "--destination"):
            destinationport = arg
    print 'Copying ' + sourceport + ' config to ' + destinationport
    result = comware.CLI('display current-configuration interface ' + sourceport, False) 
    script = []
    for line in result.get_output():
        if '#' not in line:
             if 'interface' not in line: script.append(line)
    command = 'system-view ; interface ' + destinationport + ' ; default ;'
    for line in script:
        command = command + line + ' ;'
    comware.CLI(command)

if __name__ == "__main__":
   main(sys.argv[1:])
