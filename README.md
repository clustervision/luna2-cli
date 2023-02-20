# luna2-cli

Luna 2 CLI is a part of the Luna 2 Project.<br />
Luna 2 CLI is a Command Line Interface, And used to interact with Luna 2 Daemon over Microservices.<br />
It will use REST API's to communicate to the daemon.<br />
Luna2 CLI's Prime location is Cluster, but also can be installed on the nodes.<br />

## Installation

pip install luna

## Usage
* -h or --help can be run anywhere to see the required parameters.
* -R or --raw will be useful to see the data in json while using list or show arguments.
* -i or --init will be useful while add, update, rename, clone or delete activity.
-i will provide the interactive way to perform these operations.]

## Commands Cluster
1. List of cluster with controllers
```
luna cluster list
```
2. Detaild view of cluster and controllers
```
luna cluster show {Cluster Name}
```
3. Update the Cluster information.
```
luna cluster update -n {Cluster Name} -u {Cluster User} -ntp {NTP Server IP} -d {Cluster Debug Mode} -c {Technical Contact} -pm {Provision Method} -fb {Provision Fallback}
```
## Commands Network
1. List of all configured networks
```
luna network list
```
2. Detaild view of a network
```
luna network show {Network Name}
```
3. Add a network.
```
luna network add -n {Network Name} -N {Network} -g {Gateway} -ni {NS IP} -nh {NS Hostname} -ntp {NTP Server IP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
4. Update a network.
```
luna network update -n {Network Name} -N {Network} -g {Gateway} -ni {NS IP} -nh {NS Hostname} -ntp {NTP Server IP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
5. Clone a network.
```
luna network clone -n {Network Name} -nn {New Network Name} -N {Network} -g {Gateway} -ni {NS IP} -nh {NS Hostname} -ntp {NTP Server IP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
6. Rename a network.
```
luna network rename -n {Network Name} -nn {New Network Name}
```
7. Delete a network.
```
luna network delete -n {Network Name} 
```
8. Get a Information of an IP, such as it is free or taken.
```
luna network ipinfo {Network Name} {IP Address}
```
9. Get next available IP on the network.
```
luna network nextip {Network Name}
```