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
luna cluster update -n {Cluster Name} -u {Cluster User} -ntp {NTP Server IP} -cd {Cluster Debug Mode} -c {Technical Contact} -pm {Provision Method} -fb {Provision Fallback}
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

## Commands OS Image
1. List of all os images
```
luna osimage list
```
2. Detaild view of a os images
```
luna osimage show {OSImage Name}
```
3. Add a os images.
```
luna osimage add -n {OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystems} -ge {Grab Filesystems} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -v {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
4. Update a os images.
```
luna osimage add -n {OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystems} -ge {Grab Filesystems} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -v {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
5. Clone a os images.
```
luna osimage add -n {OSImage Name} -n {New OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystems} -ge {Grab Filesystems} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -v {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
6. Rename a os images.
```
luna osimage add -n {OSImage Name} -n {New OSImage Name} 
```
7. Delete a os images.
```
luna osimage delete -n {OSImage Name} 
```
8. Pack a os images.
```
luna osimage pack {OSImage Name}
```
9. Change Kernel in an os images.
```
luna osimage kernel -n {OSImage Name}  -rd {InitRD File} -k {Kernel File} -v {Kernel Version}
```

## Commands BMC Setup
1. List of all configured BMC Setup
```
luna bmcsetup list
```
2. Detaild view of a BMC Setup
```
luna bmcsetup show {BMC Setup Name}
```
3. Add a BMC Setup.
```
luna bmcsetup add -n {BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nc {Network Channel} -mc {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
4. Update a BMC Setup.
```
luna bmcsetup update -n {BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nc {Network Channel} -mc {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
5. Clone a BMC Setup.
```
luna bmcsetup clone -n {BMC Setup Name} -nn {New BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nc {Network Channel} -mc {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
6. Rename a BMC Setup.
```
luna bmcsetup rename -n {BMC Setup Name} -nn {New BMC Setup Name}
```
7. Delete a BMC Setup.
```
luna bmcsetup delete -n {BMC Setup Name} 
```

## Commands Switch
1. List of all configured Switch
```
luna switch list
```
2. Detaild view of a Switch
```
luna switch show {Switch Name}
```
3. Add a Switch.
```
luna switch add -n {Switch Name} -N {Network} -ip {IP Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
4. Update a Switch.
```
luna switch update -n {Switch Name} -N {Network} -ip {IP Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
5. Clone a Switch.
```
luna switch clone -n {Switch Name} -nn {New Switch Name} -N {Network} -ip {IP Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
6. Rename a Switch.
```
luna switch rename -n {Switch Name} -nn {New Switch Name}
```
7. Delete a Switch.
```
luna switch delete -n {Switch Name}
```

## Commands Other Devices
1. List of all configured Other Devices
```
luna otherdevices list
```
2. Detaild view of a Other Devices
```
luna otherdevices show {Other Devices Name}
```
3. Add a Other Devices.
```
luna otherdevices add -n {Other Devices Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
4. Update a Other Devices.
```
luna otherdevices update -n {Other Devices Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
5. Clone a Other Devices.
```
luna otherdevices clone -n {Other Devices Name} -nn {New Other Devices Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
6. Rename a Other Devices.
```
luna otherdevices rename -n {Other Devices Name} -nn {New Other Devices Name}
```
7. Delete a Other Devices.
```
luna otherdevices delete -n {Other Devices Name}
```

## Commands Group
1. List of all configured Group
```
luna group list
```
2. Detaild view of a Group
```
luna group show {Group Name}
```
3. Add a Group.
```
luna group add -n {Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName} -c {Comment}
```
4. Update a Group.
```
luna group update -n {Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName} -c {Comment}
```
5. Clone a Group.
```
luna group clone -n {Group Name} -nn {New Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName} -c {Comment}
```
6. Rename a Group.
```
luna group rename -n {Group Name} -nn {New Group Name}
```
7. Delete a Group.
```
luna group delete -n {Group Name}
```
8. Get a list of all Group Interfaces of a group.
```
luna group interfaces {Group Name}
```
9. Get a Detail of a  Interface of a group.
```
luna group interface {Group Name} {Interface Name}
```
10. Update a Group Interface.
```
luna group updateinterface -n {Group Name} -if {Interface Name} -N {Network Name}
```
11. Delete a Group Interface.
```
luna group deleteinterface -n {Group Name} -if {Interface Name}
```

## Commands Node
1. List of all configured Node
```
luna node list
```
2. Detaild view of a Node
```
luna node show {Node Name}
```
3. Add a Node.
```
luna node add -n {Node Name} -host {Hostname} -g {Group Name} -lb {Local Boot} -m {Mac Address} -sw {Switch Name} -sp {Switch Port} -ser {Service} -b {BMC Setup} -s {Status} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName|IPAddress|MACAddress} -c {Comment}
```
4. Update a Node.
```
luna node update -n {Node Name} -host {Hostname} -g {Group Name} -lb {Local Boot} -m {Mac Address} -sw {Switch Name} -sp {Switch Port} -ser {Service} -b {BMC Setup} -s {Status} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName|IPAddress|MACAddress} -c {Comment}
```
5. Clone a Node.
```
luna node clone -n {Node Name} -nn {New Node Name} -host {Hostname} -g {Group Name} -lb {Local Boot} -m {Mac Address} -sw {Switch Name} -sp {Switch Port} -ser {Service} -b {BMC Setup} -s {Status} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -if {InterfaceName|NetworkName|IPAddress|MACAddress} -c {Comment}
```
6. Rename a Node.
```
luna node rename -n {Node Name} -nn {New Node Name}
```
7. Delete a Node.
```
luna node delete -n {Node Name}
```
8. Get a list of all Node Interfaces of a node.
```
luna node interfaces {Node Name}
```
9. Get a Detail of a  Interface of a node.
```
luna node interface {Node Name} {Interface Name}
```
10. Update a Node Interface.
```
luna node updateinterface -n {Node Name} -if {Interface Name} -N {Network Name} -ip {IP Address} -m {MAC Address}
```
11. Delete a Node Interface.
```
luna node deleteinterface -n {Node Name} -if {Interface Name}
```

## Commands Secrets
1. List of all Secrets
```
luna secrets list
```
2. List of all Node Secrets OR One Secret by name
```
luna secrets list node {Node Name} -s {Secret Name}
```
3. List of all Group Secrets OR One Secret by name
```
luna secrets list group {Group Name} -s {Secret Name}
```
4. Details of all Node Secrets OR One Secret by name
```
luna secrets show node {Node Name} -s {Secret Name}
```
5. Details of all Group Secrets OR One Secret by name
```
luna secrets show group {Group Name} -s {Secret Name}
```
6. Update of all Node Secrets OR One Secret by name
```
luna secrets update node -n {Node Name} -s {Secret Name} -c {Content} -p {Path}
```
7. Update of all Group Secrets OR One Secret by name
```
luna secrets update group -n {Group Name} -s {Secret Name} -c {Content} -p {Path}
```
8. Clone a Node Secret.
```
luna secrets clone node -n {Node Name} -nn {New Secret Name} -s {Secret Name} -c {Content} -p {Path}
```
9. Clone a Group Secret.
```
luna secrets clone group -n {Group Name} -nn {New Secret Name -s {Secret Name} -c {Content} -p {Path}
```
10. Delete a Node Secret.
```
luna secrets delete node -n {Node Name} -s {Secret Name}
```
11. Delete a Group Secret.
```
luna secrets delete group -n {Group Name} -s {Secret Name} 
```

## Commands Service
1. Perform action on DHCP Service
```
luna service dhcp {start/stop/restart}
```
2. Perform action on DNS Service
```
luna service dns {start/stop/restart}
```
3. Perform action on Luna 2 Daemon Service
```
luna service luna2 {start/stop/restart}
```
## Commands Control [WIP]
