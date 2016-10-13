from netmiko import ConnectHandler

A3810_1 = {
    'device_type':'hp_procurve',
    'ip':'10.150.0.1',
    'username':'ctrask',
    'password':'timshel',
}

net_connect = ConnectHandler(**A3810_1)

output = net_connect.send_command("display clock")

print output