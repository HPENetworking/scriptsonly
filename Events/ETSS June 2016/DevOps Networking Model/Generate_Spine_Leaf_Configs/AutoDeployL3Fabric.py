import requests
import yaml
import githubuser
from pyhpeimc.auth import *
from pyhpeimc.plat.device import *
from pyhpeimc.plat.icc import *
from pyhpeimc.plat.vlanm import *
from jinja2 import Environment, FileSystemLoader, Template

#credentials for IMC server, change to meet your environment
auth = IMCAuth("http://", "10.101.0.203", "8080", "admin", "admin")


ENV = Environment(loader=FileSystemLoader('./'))

with open("globalvals.yaml") as inputfile:
    devglobals =  yaml.load(inputfile)

with open('devices.yaml') as inputfile:
    devs = yaml.load(inputfile)

for dev in devs:
    if dev['role'] == "spine":
        template = ENV.get_template("7900_spine.j2")
        #print (template.render(devglobals=devglobals, dev=dev))
        cmd_list = ['system-view']
        cmd_list = cmd_list + template.split('\n')
        devid = get_dev_details(dev['interfaces'][0]['ipaddress'], auth.creds, auth.url)['id']
        run_dev_cmd(devid, cmd_list, auth.creds, auth.url)['success']



        #with open(dev['sysname']+".cfg", "w") as file:
         #  file.write(template.render(devglobals=devglobals, dev=dev))
    if dev['role'] == "leaf":
        template = ENV.get_template("5930_leaf.j2")
        cmd_list = ['system-view']
        cmd_list = cmd_list + template.split('\n')
        devid = get_dev_details(dev['interfaces'][0]['ipaddress'], auth.creds, auth.url)['id']
        run_dev_cmd(devid, cmd_list, auth.creds, auth.url)['success']


    #print (template.render(devglobals=devglobals, dev=dev))
    #with open(dev['sysname']+".cfg", "w") as file:
     #   file.write(template.render(devglobals=devglobals, dev=dev))

# Print dictionary generated from yaml    


# Render template and print generated config to console
#template = ENV.get_template("Comware5_Template.j2")
#print (template.render(network_global=network_global, device_values = device_values, site= site))

