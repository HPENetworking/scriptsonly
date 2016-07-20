
We've looked at generating configurations for a single device, but what happens if we want to start generating standardized configurations for a group of devices, say a data center fabric?

Well Jinja2, YAML, and a bit of python code can help you with that as well!


First, let's get all our initial imports out of the way and set the environment variable, you'll notice I'm actually loading the env in a subdirectory here


```python
from jinja2 import Environment, FileSystemLoader, Template
import yaml
import json
ENV = Environment(loader=FileSystemLoader('./Generate_Spine_Leaf_Configs'))
import os
```

## Global Values

In most environments, there are a lot of values that are identical between network devices, some of these may include
- SNMP Settings
- Usernames and Passwords
- SNMP Trap Receiver
- SYSLOG Server
- NTP Server
- Etc.

Part of the power of automation is to not repeat yourself more than you have to right? So the first thing we do is split apart the device specific elements of the configurations vs. the elements that are global, or shared between the  different devices.

To do that we've created two files, one called **globalvals.yaml** which we'll look first, and then one called **devs** which we will take a look at below.

## Examining **globalvals**

Now that we've loaded the **globalvals.yaml** file into a python dictionary called **devglobals** let's take a quick look and see what's in here. We're going to first convert it back to YAML and then print it out. YAML's a little easier to read for human beings which is why we use it so much. 


Looking at the output below, you can see we've got sections for 
- ecmpmode
- ospf
- snmp
- users
- vlans

If you're reading this, I'm assuming you're a network professional and I'm guessing I don't need to explain what any of these pieces actually are. It's all pretty straight forward, but if I've guessed wrong, please let me know in the comments. 



```python
with open("./Generate_Spine_Leaf_Configs/Inputs/globalvals.yaml") as inputfile:
    devglobals =  yaml.load(inputfile)

```


```python
print (yaml.dump(devglobals, indent = 4))
```

    ecmpmode: enhanced
    ospf: {area: 0, network: 192.168.0.0, process: 1, wildcard: 0.0.255.255}
    snmp:
        read: public
        syscontact: admin.lab.local
        syslocation: lab
        trap:
        - {target: 10.10.10.10}
        write: private
    users:
    - {password: admin, username: admin}
    vlans:
    - {description: management vlan, id: '10', name: management}
    - {description: users vlan, id: '15', name: users}
    - {description: phones vlan, id: '16', name: phones}
    - {description: servers vlan, id: '20', name: servers vlan}
    


## Examining **devices.yaml**

Now that we've loaded the **devices.yaml** file into a python dictionary called **devs** let's take a quick look and see what's in here. We're going to first convert it back to YAML and then print it out. YAML's a little easier to read for human beings which is why we use it so much. 


Looking at the output below, you can see we've got sections for four sections, each of which are describing the unique values for four different switches. If you're following along at home, the switches are named
- 7904-1
- 7904-2
- 5930-1
- 5930-3

If you look at each individual switch, they all have the same attributes which I'm pretty sure you'll understand exactly what they're doing if you take a few moments to read through them.

- interfaces
- oobm
- role
- routerid
- sysname
- type




```python
with open("./Generate_Spine_Leaf_Configs/Inputs/devices.yaml") as inputfile:
    devs =  yaml.load(inputfile)

```


```python
print (yaml.dump(devs, indent = 4))
```

    -   interfaces:
        - {description: LoopBack0, ifdesc: LoopBack0, ipaddress: 192.168.1.1, mask: 255.255.255.255}
        - {description: OOBM Interface, ifdesc: M-GigabitEthernet1/0/0/0, ipaddress: 10.10.10.40,
            mask: 255.255.255.0}
        - {description: link to 5930-2, ifdesc: Ten-GigabitEthernet1/2/0/3, ipaddress: 192.168.2.5,
            mask: 255.255.255.252, portmode: route}
        - {description: link to 5930-1, ifdesc: Ten-GigabitEthernet1/2/0/4, ipaddress: 192.168.2.1,
            mask: 255.255.255.252, portmode: route}
        oobm: 10.10.10.40
        role: spine
        routerid: 192.168.1.1
        sysname: 7904-1
        type: 7900
    -   interfaces:
        - {description: LoopBack0, ifdesc: LoopBack0, ipaddress: 192.168.1.2, mask: 255.255.255.255}
        - {description: OOBM Interface, ifdesc: M-GigabitEthernet1/0/0/0, ipaddress: 10.10.10.41,
            mask: 255.255.255.0}
        - {description: link to 5930-2, ifdesc: Ten-GigabitEthernet1/2/0/3, ipaddress: 192.168.2.13,
            mask: 255.255.255.252, portmode: route}
        - {description: link to 5930-1, ifdesc: Ten-GigabitEthernet1/2/0/4, ipaddress: 192.168.2.9,
            mask: 255.255.255.252, portmode: route}
        oobm: 10.10.10.41
        role: spine
        routerid: 192.168.1.2
        sysname: 7904-2
    -   interfaces:
        - {description: LoopBack0, ifdesc: LoopBack0, ipaddress: 192.168.1.11, mask: 255.255.255.255}
        - {description: OOBM Interface, ifdesc: M-GigabitEthernet0/0/0, ipaddress: 10.10.10.42,
            mask: 255.255.255.0}
        - {description: link to 7904-2, ifdesc: Ten-GigabitEthernet1/1/1, ipaddress: 192.168.2.10,
            mask: 255.255.255.252, portmode: route}
        - {description: link to 7904-1, ifdesc: Ten-GigabitEthernet1/1/2, ipaddress: 192.168.2.2,
            mask: 255.255.255.252, portmode: route}
        oobm: 10.10.10.42
        role: leaf
        routerid: 192.168.1.11
        sysname: 5930-1
    -   interfaces:
        - {description: LoopBack0, ifdesc: LoopBack0, ipaddress: 192.168.1.12, mask: 255.255.255.255}
        - {description: OOBM Interface, ifdesc: M-GigabitEthernet0/0/0, ipaddress: 10.10.10.43,
            mask: 255.255.255.0}
        - {description: link to 5930-2, ifdesc: Ten-GigabitEthernet1/1/1, ipaddress: 192.168.2.14,
            mask: 255.255.255.252, portmode: route}
        - {description: link to 5930-1, ifdesc: Ten-GigabitEthernet1/1/2, ipaddress: 192.168.2.6,
            mask: 255.255.255.252, portmode: route}
        oobm: 10.10.10.43
        role: leaf
        routerid: 192.168.1.12
        sysname: 5930-2
    


## Rendering the Configurations

Now that we've loaded the two YAML files, we're going to use them as input into the Jinja2 templates that are located in the template directory. 

Looking at the code below, we're executing the following logic

1) For each switch in the devs file ( remember there were four right? )
2) If the "role" key of the devices has a value of **spine** then render the configuration included in the template **7900_spine.j2** and write it to disk using the value of the "sysname" key.
3) If the "role key of the devices has a value of **leaf** then render the configuration included in the template **5930_leaf.j2** and write it to disk using the value of the "sysname" key. 

But before we do that, let's take a look in the Configs directory to make sure it's currently empty and I"m not plaing any tricks here. 



```python
dirlist = os.listdir("./Generate_Spine_Leaf_Configs/Configs")
print (dirlist)
```

    []


Now we generate the configurations


```python
for dev in devs:
    if dev['role'] == "spine":
        template = ENV.get_template("./Templates/7900_spine.j2")
        #print (template.render(devglobals=devglobals, dev=dev))
        with open("./Generate_Spine_Leaf_Configs/Configs/"+dev['sysname']+".cfg", "w") as file:
            file.write(template.render(devglobals=devglobals, dev=dev))
    if dev['role'] == "leaf":
        template = ENV.get_template("./Templates/5930_leaf.j2")
    #print (template.render(devglobals=devglobals, dev=dev))
    with open("./Generate_Spine_Leaf_Configs/Configs/"+dev['sysname']+".cfg", "w") as file:
        file.write(template.render(devglobals=devglobals, dev=dev))
```


```python
dirlist = os.listdir("./Generate_Spine_Leaf_Configs/Configs")
print (dirlist)
```

    ['5930-1.cfg', '5930-2.cfg', '7904-1.cfg', '7904-2.cfg']


##  Verifying the Configs

I'll leave it to the reader to take a look at the configurations to see exactly what the differences are, but to give you a quick taste, here's the compare screen capture from my pycharm IDE.

The differences are automatically highlited in blue making it easy to see that other than the unique values which come ouf of the **devices.yaml** file, all of the configurations are standardized.  

And the best part? If you want to change one of the global values? You just change it in a single place and it automatically will become part of the new configurations once you re-render the templates.

![Config Diffs](./images/configdiffs.png)



# Where to next?

Templating is cool and incredibly useful in cutting down on the amount of repetitive config commands that you're probably typing by hand today. You may be slightly more advanced and using a good ol' cut-and-paste between files, but there's always the opportunity for human error when you're retyping the unique device values, not to mention the fact that you're going to have to cut and paste that a lot of times.

As well, as we saw previously, the values in the **.YAML** files are not really unique to any particular vendor, so if you're looking to make a change, all you would have to do is to generate the jinja2 templates for your new manufacturer of choice and your new configurations could be moved over with minimal effort. 

Choice is always good right?  If you're staying with your current network vendor, it should be because you're happy with the overall experience, not because it's too hard to change to anything else. 

@netmanchris
