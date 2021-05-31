from netmiko import ConnectHandler
import telnetlib
import time
R = '\033[31m'  # red
O = '\033[33m'  # orange
W = '\033[0m'  # white (normal)

print(R+'BEFORE RUNNING THE SCRIPT MAKE SURE THE LAB IS LOADED INTO YOUR EVE-NG INSTANCE')
print(O+'CHECK IF ALL VMs INSIDE EVE-NG ARE RUNNING')
time.sleep(3)

srvip = input(W+'Enter your EVE-NG instance IP (ex:172.16.208.X):')

# Configure Devices

devices = [
    [
        {
            'device_type': 'cisco_ios_telnet',
            'host': srvip,
            'port': '32769',
        },
        [
            'hostname D1',
            'banner motd # D1, Tuning EtherChannel #',
            'spanning-tree mode rapid-pvst',
            'line con 0',
            'exec-timeout 0 0',
            'logging synchronous',
            'exit',
            'interface range e1/0-3',
            'switchport trunk encapsulation dot1q',
            'switchport mode trunk',
            'no shutdown',
            'exit',
            'clock timezone UTC +0'
        ]
    ],
    [
        {
            'device_type': 'cisco_ios_telnet',
            'host': srvip,
            'port': '32770',
        },
        [
            'hostname D2',
            'banner motd # D2, Tuning EtherChannel #',
            'spanning-tree mode rapid-pvst',
            'line con 0',
            'exec-timeout 0 0',
            'logging synchronous',
            'exit',
            'interface range e1/0-3',
            'switchport trunk encapsulation dot1q',
            'switchport mode trunk',
            'no shutdown',
            'exit',
            'clock timezone UTC +0'
        ]
    ]
]

for dv in devices:
    print('Connecting to device ' + str.split(dv[1][0])[1] + '...')
    # Equipment Connection using the dict
    con = ConnectHandler(**dv[0])
    print('Configuring device ' + str.split(dv[1][0])[1] + '...')
    con.find_prompt()
    con.enable('enable')
    con.config_mode('conf t')
    # Configuring the equipment with the command in the second element of the list
    output = con.send_config_set(dv[1])
    con.disconnect()
    print('#################################################################')


print('Lab 5.1.4 CCNP ENCOR is loaded with the initial configuration')
print('Enjoy and good work')
