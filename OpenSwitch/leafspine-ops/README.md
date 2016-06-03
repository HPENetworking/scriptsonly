# OpenSwitch automation environment demo

This demo targets creation of leaf-spine OpenSwitch topology in virtualized automated environment within single host OS leveraging Docker and Docker Networking. After environment is created you can connect to switches in topology and test various settings, APIs or web UI. Main purpose is to demo Ansible automated configuration of L3 fabric.

## Steps to build your OpenSwitch L3 fabric within Docker host

1. Prepare Linux VM with Docker as only dependency
2. Chmod +x scripts so you can execute them
3. Open create.sh and change arrays to fit your needs. By default 4 leafs and 2 spines are created, but you can change this by adding or removing device names from arrays on first three lines.
4. Run create.sh to create your topology and run containers (see sections bellow for details)
5. Setup Ansible environment (make sure you use Ansible 2.1) and test connectivity to switches by running test-connection.yml playbook
6. Use script to compile your fabric topology file (future)
7. Execute Ansible playbook build-fabric.yml leveraging your fabric topology file to automate creation of L3 BGP-based fabric configuration
8. Execute Ansible playbook test-fabric.yml to ensure BGP peering is estabilished

## Topology creation script

There are many ways to test OpenSwitch in varius topologies including using OVA virtual machines (perhaps automated with Vagrant), physical switches or Mininet. I find using Docker and Docker Networking (to create inter-switch links) easiest to use, efficient and isolated as it all runs inside single Linux VM.

### Using create.sh

Simply setup VM and install Docker as only dependecy. Copy create.sh and run

    chmod +x create.sh

to make it executable. By default create.sh will build topology of 4 leafs and 2 spines. To change this you can edit arrays in file by adding or removing hostnames. For example this creates topology of 4 leafs and 4 spines:

    switches=(leaf1 leaf2 leaf3 leaf4 spine1 spine2 spine3 spine4)
    leafs=(leaf1 leaf2 leaf3 leaf4)
    spines=(spine1 spine2 spine3 spine4)

You need to have OpenSwitch Docker image available. You can compile your own (will document later + you can find details on project web site) or for start reference one I have posted to Docker Hub (I strongly recommend to get your own with latest code). You can specify image name on fourth line in create.sh:

    dockerimage="cloudsvet/openswitch:0525"

After you run create.sh script will
* Create out-of-band management network (you can use it from inside of machine to access SSH, UI or APIs)
* Run OpenSwitch instances as Docker containers
* Create Docker networks and attach to containers to provide inter-switch links (port numbers are always leaf1 port 1 to spine1 port 1, leaf1 port 2 to spine2 port 1, leaf2 port 1 to spine1 port 2 etc.)
* Connect to OpenSwitch instances and move "front port" interfaces to OpenSwitch namespace, so those are visible as front ports
* Prepare Ansible hosts file and write it to disk as hosts (also you will see it printed on your screen with IP addresses of your switches - you can use it from within your VM to connect to switches)

### Using destroy.sh

After you are done with playing use destroy.sh to clean everything up. This script kills and deletes your containers and Docker networks.

## Using environment with Ansible

Main purpose of this demo setup is to play with Ansible. First thing you need to do is install Ansible 2.1, which is first version to introduce OpenSwitch modules.

Hosts file has been generated for you by create.sh

Linux typically want you to store SSH public keys of systems you are connecting to and throws error message when those change. Everytime you recreate your environment this happens. For purpose of demo you can disable this by creating (or modifying existing) settings file in ~/.ssh/config:

    Host *
        StrictHostKeyChecking no
        UserKnownHostsFile /dev/null

In my case OpenSwitch did not come with SFTP enabled so I rather instructed Ansible to use SCP. You can do this by executing this in your shell:

    export ANSIBLE_SCP_IF_SSH=y

Now you can execute Ansible playbook test-connection.yml referencing hosts file created by create.sh:

    ansible-playbook -i hosts test-connection.yml

If everything is OK, you will see Ansible being able to "ping" switches and Playbook runs OpenSwitch module to get device information and print version of your individual switches.

Also note that you can use --limit to run this on one group only (leafs or spines) or target just one individual switch (such as leaf1).

Security notice: in our example we are using root access with no password. This is definitelly not a good practice for real life. You should use key-based authentication only and disable password access. There are hints how to do this initial setup via Ansible or using initial zero touch provisioning of your real switches.

## Automation with Ansible

create.sh script has created hosts file that describes your virtual topology for Ansible.

This demo is based on switch and bgp Ansible roles prepared by Nohguchi, Kei <kei.nohguchi@hpe.com> (Thanks!). Those are under review to be accepted in ops-ansible project as official roles.

First step is to define your logical topology model. In order for Ansible to have information about your desired logical topology you need to describe it in vars/topology.yml file. You are listing switches there (identified by hostname) and in YAML structure define their AS number, interfaces and associated IP addresses. In future I would like to provide script to automatically create this initial topology model (it helps with model by automatically assigning AS numbers and IPs in incrementing fashion - good for initial document, but afterwards is better to stick with resulting file to prevent potential unnecessary readresing etc.)

Now you are ready to build your fabric.

Execute Playbook to build fabric.

    ansible-playbook -i hosts build-fabric.yml

Now you may want to check that your peering is correctly estabilished (means check not only configuration, but actual control plane state). There is playbook to do just that and report state of BGP neighbors.

    ansible-playbook -i hosts test-fabric.yml

## How to demo

Here is example workflow to demo OpenSwitch, Ansible, ops-ansible roles and desired state principles.

Source Ansible environment variable
    . envrc

Create virtual network
    ./create.sh

Wait a moment and execute Playbook to test connectivity and print OpenSwitch version
    ansible-playbook -i hosts test-connection.yml

Connect to one of devices directly and show that configuration is empty
docker exec -ti leaf1 vtysh
    switch# show run
    Current configuration:

    vlan 1
        no shutdown
    switch# exit

Make your fabric come to your desired state
    ansible-playbook -i hosts build-fabric.yml

Test all peering are in Estabilished state (if not you might just wait for BGP to catch up a re-run)
    ansible-playbook -i hosts test-fabric.yml

Connect to one of switches and misconfigure remote-as of one of neighbors
    docker exec -ti leaf1 vtysh
    leaf1# show run
    Current configuration:

    hostname leaf1

    router bgp 65001
         bgp router-id 192.168.0.1
         network 192.168.0.1/32
         neighbor 10.1.0.2 remote-as 65101
         neighbor 10.2.0.2 remote-as 65102

    vlan 1
        no shutdown
    interface 1
        no shutdown
        ip address 10.1.0.1/30
    interface 2
        no shutdown
        ip address 10.2.0.1/30
    interface loopback 1
        ip address 192.168.0.1/32

    leaf1# conf t
    leaf1(config)# router bgp 65001
    leaf1(config-router)# neighbor 10.1.0.2 remote-as 65999
    leaf1(config-router)# end
    leaf1# exit

Re-run testing Playbook to show that there are non-estabilished peers
    ansible-playbook -i hosts test-fabric.yml
    ...
    TASK [Report switches with failed neighbors] ***********************************
    skipping: [spine2] => (item=Peering to 10.2.0.1 is Established
    )
    skipping: [spine2] => (item=Peering to 10.2.1.1 is Established
    )
    failed: [spine1] (item=Peering to 10.1.0.1 is Idle
    ) => {"failed": true, "item": "Peering to 10.1.0.1 is Idle\n", "msg": "Peering to 10.1.0.1 is Idle\n"}
    skipping: [spine1] => (item=Peering to 10.1.1.1 is Established
    )
    skipping: [spine1] => (item=Peering to 10.1.2.1 is Established
    )
    skipping: [spine1] => (item=Peering to 10.1.3.1 is Established
    )
    skipping: [spine2] => (item=Peering to 10.2.2.1 is Established
    )
    skipping: [leaf2] => (item=Peering to 10.1.1.2 is Established
    )
    skipping: [leaf2] => (item=Peering to 10.2.1.2 is Established
    )
    skipping: [leaf3] => (item=Peering to 10.1.2.2 is Established
    )
    skipping: [leaf3] => (item=Peering to 10.2.2.2 is Established
    )
    skipping: [spine2] => (item=Peering to 10.2.3.1 is Established
    )
    skipping: [leaf4] => (item=Peering to 10.1.3.2 is Established
    )
    failed: [leaf1] (item=Peering to 10.1.0.2 is Deleted
    ) => {"failed": true, "item": "Peering to 10.1.0.2 is Deleted\n", "msg": "Peering to 10.1.0.2 is Deleted\n"}
    skipping: [leaf4] => (item=Peering to 10.2.3.2 is Established
    )
    skipping: [leaf1] => (item=Peering to 10.2.0.2 is Established
    )

Re-rub build-fabric Playbook to put network into desired state again
    ansible-playbook -i hosts build-fabric.yml

You can check switch configuration was repaired
    docker exec -ti leaf1 vtysh
    leaf1# show run

You can re-run testing playbook to make sure all neighbours are in Estabilished state (please note that this might take a while)
    ansible-playbook -i hosts test-fabric.yml

## Roadmap

I will try to add Ansible Playbook example to do automated BGP-based L3 fabric setup. My plan is the following:
* Create script to generate topology file for Ansible. You will input parameters such as Leaf-Spine interlinks starting IP addresses, starting BGP AS number for Leafs, starting BGP AS number for spines, starting port number for leaf-spine connections etc. Based on this and hosts file generated by create.sh script will generate fabric topology described as YAML file to be consumed by Ansible playbook

Also at some point I would like to look into setting up real fabric with zero touch provisioning (DHCP server with reservations, web server for accessing OS binary etc.) + generating hosts file for Ansible.
