from netmiko import ConnectHandler
from datetime import datetime

MSR1K_1 = {
    'device_type':'hp_comware',
    'ip':'10.150.0.2',
    'username':'ctrask',
    'password':'timshel',
}

A3810_1 = {
    'device_type':'hp_procurve',
    'ip':'10.150.0.1',
    'username':'ctrask',
    'password':'timshel',
}

tin = [A3810_1, MSR1K_1]


start_time = datetime.now()
print start_time
fail_list = []
for x in tin:
    net_connect = ConnectHandler(**x)
    output = net_connect.send_command("display arp")
    name = net_connect.find_prompt() + x['ip']
#    print "\n\n>>>>>>>>>>>>>>>{0}<<<<<<<<<<<<<<<<<<<<".format(x['ip'])
    print "\n\n>>>>>>>>>>>>>>>{0}<<<<<<<<<<<<<<<<<<<<".format(name)
    print output
    if '10.150.0.254' in output:
        print "GATEWAY OK"
    else:
        print "GATEWAY UNKNOWN"
        fail_list.append(x['ip'])

    print (">>>>>>>>>>>>>>>>>>>>>End<<<<<<<<<<<<<<<<<<<<<<")

end_time = datetime.now()
print end_time
if fail_list != []:
    print "\nThese devices failed:"
    print fail_list
else:
    print "\n\nAll devices OK"
