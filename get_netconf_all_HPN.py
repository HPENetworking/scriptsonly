#!/usr/bin/env python

'''
This is simple script to retrieve all information from HPN switch or router via NETCONF over SSH.
This program can be easily extended to meet your own requirements. I have developed the program with
HP Network simulator. When this program is used against physical HP Comware Network switches
please change h3c.com in hp.com.
'''

__author__ = "Dobias van Ingen"
__credits__ = "Jason Edelman for insipring me in creating this program (http://www.jedelman.com/)"
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "Dobias van Ingen"
__email__ = "dobias.vaningen@gmail.com"

from ncclient import manager
import xml.dom.minidom



def connect(host, username, password):
    # Set-up connection to device
    with manager.connect(host=host,
                        port=830,
                        username=username,
                        password=password,
                        hostkey_verify=False,
                        allow_agent=False,
                        look_for_keys=False
                        ) as netconf_manager:

        data = netconf_manager.get()
    return data


if __name__ == '__main__':
    # Set-up connection
    connection = connect('192.168.56.12', 'dobias', 'HPR0cks')

    # Let's print output more pretty
    x = connection.data_xml
    xml = xml.dom.minidom.parseString(x)
    pretty_xml = xml.toprettyxml()
    
    print( pretty_xml )
