from netmiko import ConnectHandler
import telnetlib
import time
import os
import sys

# Function to inport from file a list of devices to configure
# Once the list is loaded the name os the devices conrresponds to a file name with its configuration


def device_config(dev):
    for dv in dev:
        con = {'device_type': 'cisco_ios_telnet', 'host': srvip, 'port': ''}
        con['port'] = dv[1]

        print('Connecting to device ' + dv[0] + '...')

        # Equipment Connection using the dict
        con = ConnectHandler(**con)
        print('Configuring device ' + dv[0] + '...')
        con.find_prompt()
        con.enable('enable')
        con.config_mode('conf t')
        # Configuring the equipment with the commands in the filename from the device list
        try:
            configs = []
            with open(os.path.join(sys.path[0], "%s.txt" % dv[0])) as f:
                for line in f:
                    print(line.replace("\n", ""))
                    time.sleep(0.1)
                    configs.append(line)
        except IOError:
            print("No configs loaded")
        con.send_config_set(configs)
        con.disconnect()
        print('#################################################################')


def host_config(vpcs):
    for pc in vpcs:
        print('Configuring ' + pc[0])
        # Telnet Connection
        tn = telnetlib.Telnet(host=srvip, port=pc[1])
        time.sleep(1)
        tn.read_until(b'> ')

        # Change VPCS name
        setname = 'set pcname ' + pc[0]
        tn.write(setname.encode() + b'\n')
        print('Changing VPCS name to ' + pc[0])
        time.sleep(1)

        # Change ipv4 Address
        tn.write(pc[2].encode() + b'\n')
        print('Changing ' + pc[0] + ' ipv4 configuration to ' + pc[2])
        time.sleep(1)

        # Change ipv6 Address
        tn.write(pc[3].encode() + b'\n')
        print('Changing ' + pc[0] + ' ipv6 configuration to ' + pc[3])
        time.sleep(1)

        print('#################################################################')


R = '\033[31m'  # red
O = '\033[33m'  # orange
W = '\033[0m'  # white (normal)

print(R+'BEFORE RUNNING THE SCRIPT MAKE SURE THE LAB IS LOADED INTO YOUR EVE-NG INSTANCE')
print(O+'CHECK IF ALL VMs INSIDE EVE-NG ARE RUNNING')
time.sleep(3)

srvip = input(W+'Enter your EVE-NG instance IP (ex:172.16.208.X):')

# Device Config
try:
    devices = []
    with open(os.path.join(sys.path[0], "devices.txt")) as f:
        for line in f:
            list = []
            list = line.split()
            # Configure Devices
            devices.append(list)
    device_config(devices)
except IOError:
    print("No devices to be configured.")

# Host Config
try:
    hosts = []
    with open(os.path.join(sys.path[0], "vpcs.txt")) as f:
        for line in f:
            list = []
            list = line.split(",")
            # Configure Devices
            hosts.append(list)
    print(hosts)
    host_config(hosts)
except IOError:
    print("No hosts to be configured.")


print('Lab 5.1.2 CCNP ENCOR is loaded with the initial configuration')
print('Enjoy and good work')
