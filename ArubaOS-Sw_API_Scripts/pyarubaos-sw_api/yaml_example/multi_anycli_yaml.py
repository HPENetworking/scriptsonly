import yaml

with open("yaml_test.yaml", 'r') as stream:
    try:
        pydata = yaml.load(stream)
        print(pydata)
        ip_addr = pydata['ip_addr']
        username = pydata['username']
        password = pydata['password']
        command = pydata['command']
    except yaml.YAMLERROR as exc:
        print(exc)

print(ip_addr)
