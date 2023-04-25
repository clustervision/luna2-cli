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
* -V or --version will be useful to see the current version of Luna.
* -V or --version will be useful to see the current version of Luna.
* -v or --verbose will be useful for debugging purpose.
* Log File location -> /var/log/luna/luna2-cli.log


## Commands Cluster
1. Detailed view of cluster and controllers
```
luna cluster
```
2. Make change in Cluster information.
```
luna cluster change -n {Cluster Name} -u {Cluster User} -ntp {NTP Server IP} -o {Create Node On Demand} -ns {Name_Server IP} -fs {Forward_Server IP} -c {Technical Contact} -pm {Provision Method} -pf {Provision Fallback} -s {Security} -d {Debug Mode}
```

## Commands Network
1. List of all configured networks
```
luna network list
```
2. Detailed view of a network
```
luna network show {Network Name}
```
3. Add a network.
```
luna network add {Network Name} -N {Network} -g {Gateway} -nsip {NS IP} -ntp {NTP Server IP} -dhcp {DHCP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
4. Make change in network information.
```
luna network change {Network Name} -N {Network} -g {Gateway} -nsip {NS IP} -ntp {NTP Server IP} -dhcp {DHCP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
5. Clone a network.
```
luna network clone {Network Name} {New Network Name} -N {Network} -g {Gateway} -nsip {NS IP} -ntp {NTP Server IP} -dhcp {DHCP} -ds {DHCP Range Start} -de {DHCP Range End} -c {Comment}
```
6. Rename a network.
```
luna network rename {Network Name} {New Network Name}
```
7. Remove a network.
```
luna network remove {Network Name} 
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
2. Detailed view of a os images
```
luna osimage show {OSImage Name}
```
3. Add a os images.
```
luna osimage add {OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystem} -ge {Grab Filesystem} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -var {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
4. Make change in a os images.
```
luna osimage change {OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystem} -ge {Grab Filesystem} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -var {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
5. Clone a os images.
```
luna osimage clone {OSImage Name} {New OSImage Name} -dm {Dracut Modules} -gf {Grab Filesystem} -ge {Grab Filesystem} -rd {InitRD File} -k {Kernel File} -m {Kernel Modules} -o {Kernel Options} -var {Kernel Version} -p {Path Of Image} -tar {Tarball UUID} -t {Torrent UUID} -D {Distribution} -c {Comment}
```
6. Rename a os images.
```
luna osimage rename {OSImage Name} {New OSImage Name} 
```
7. Remove a os images.
```
luna osimage remove {OSImage Name} 
```
8. Pack a os images.
```
luna osimage pack {OSImage Name}
```
9. Change Kernel in an os images.
```
luna osimage kernel {OSImage Name}  -rd {InitRD File} -k {Kernel File} -ver {Kernel Version}
```
10. OS Image used by nodes.
```
luna osimage member {OSImage Name}
```

## Commands BMC Setup
1. List of all configured BMC Setup
```
luna bmcsetup list
```
2. Detailed view of a BMC Setup
```
luna bmcsetup show {BMC Setup Name}
```
3. Add a BMC Setup.
```
luna bmcsetup add {BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nt {Network Channel} -mt {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
4. Make change in BMC Setup.
```
luna bmcsetup change {BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nt {Network Channel} -mt {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
5. Clone a BMC Setup.
```
luna bmcsetup clone {BMC Setup Name} {New BMC Setup Name} -uid {User ID} -u {Username} -p {Password} -nt {Network Channel} -mt {Management Channel} -ubu {Unmanaged BMC Users} -c {Comment}
```
6. Rename a BMC Setup.
```
luna bmcsetup rename {BMC Setup Name} {New BMC Setup Name}
```
7. Remove a BMC Setup.
```
luna bmcsetup remove {BMC Setup Name} 
```
8. BMC Setup used by nodes.
```
luna bmcsetup member {BMC Setup Name}
```

## Commands Switch
1. List of all configured Switch
```
luna switch list
```
2. Detailed view of a Switch
```
luna switch show {Switch Name}
```
3. Add a Switch.
```
luna switch add {Switch Name} -N {Network} -ip {IP Address} -m {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
4. Make change in a Switch.
```
luna switch change {Switch Name} -N {Network} -ip {IP Address} -m {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
5. Clone a Switch.
```
luna switch clone {Switch Name} {New Switch Name} -N {Network} -ip {IP Address} -m {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -c {Comment}
```
6. Rename a Switch.
```
luna switch rename {Switch Name} {New Switch Name}
```
7. Remove a Switch.
```
luna switch remove {Switch Name}
```

## Commands Other Devices
1. List of all configured Other Devices
```
luna otherdev list
```
2. Detailed view of a Other Device
```
luna otherdev show {Other Device Name}
```
3. Add a Other Device.
```
luna otherdev add {Other Device Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
4. Make change in a Other Device.
```
luna otherdev change {Other Device Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
5. Clone a Other Device.
```
luna otherdev clone {Other Device Name} {New Other Device Name} -N {Network} -ip {IP Address} -m {Mac Address} -c {Comment}
```
6. Rename a Other Device.
```
luna otherdev rename {Other Device Name} {New Other Device Name}
```
7. Delete a Other Device.
```
luna otherdev delete {Other Device Name}
```

## Commands Group
1. List of all configured Group
```
luna group list
```
2. Detailed view of a Group
```
luna group show {Group Name}
```
3. Add a Group.
```
luna group add {Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -O {Interface Options} -c {Comment}
```
4. Make change in a Group.
```
luna group change {Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -O {Interface Options} -c {Comment}
```
5. Clone a Group.
```
luna group clone {Group Name} {New Group Name} -b {BMC Setup} -bmc {BMC Setup Name} -D {Domain Name} -o {OS Image Name} -pre {Pre Script} -part {Part Script} -post {Post Script} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -ubu {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -O {Interface Options} -c {Comment}
```
6. Rename a Group.
```
luna group rename {Group Name} {New Group Name}
```
7. Remove a Group.
```
luna group remove {Group Name}
```
8. Get a list of all Group Interfaces of a group.
```
luna group listinterface {Group Name}
```
9. Get a Detail of a  Interface of a group.
```
luna group showinterface {Group Name} {Interface Name}
```
10. Make change in a Group Interface.
```
luna group changeinterface {Group Name} {Interface Name} -N {Network Name} -O {Interface Options}
```
11. Remove a Group Interface.
```
luna group removeinterface {Group Name} {Interface Name}
```
12. Group used by nodes.
```
luna group member {Group Name}
```

## Commands Node
1. List of all configured Node
```
luna node list
```
2. Detailed view of a Node
```
luna node show {Node Name}
```
3. Add a Node.
```
luna node add {Node Name} -host {Hostname} -g {Group Name} -o {OSImage Name} -b {BMC Setup} -bmc {BMC Setup Name} -sw {Switch Name} -sp {Switch Port} -pre {Pre Script} -part {Part Script} -post {Post Script} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -lb {Local Boot} -s {Status} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -c {Comment}-if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -O {Interface Options}

```
4. Make change in a Node.
```
luna node change {Node Name} -host {Hostname} -g {Group Name} -o {OSImage Name} -b {BMC Setup} -bmc {BMC Setup Name} -sw {Switch Name} -sp {Switch Port} -pre {Pre Script} -part {Part Script} -post {Post Script} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -lb {Local Boot} -s {Status} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -c {Comment}-if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -O {Interface Options}
```
5. Clone a Node.
```
luna node clone {Node Name} {New Node Name} -host {Hostname} -g {Group Name} -o {OSImage Name} -b {BMC Setup} -bmc {BMC Setup Name} -sw {Switch Name} -sp {Switch Port} -pre {Pre Script} -part {Part Script} -post {Post Script} -pi {Provision Interface} -pm {Provision Method} -fb {Provision Fallback} -nb {Network Boot} -li {Local Install} -bm {Boot Menu} -lb {Local Boot} -s {Status} -tid {TPM UUID} -tkey {TPM Public Key} -tsha {TPM SHA256} -ubu {Unmanaged BMC Users} -c {Comment}-if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -O {Interface Options}
```
6. Rename a Node.
```
luna node rename {Node Name} {New Node Name}
```
7. Remove a Node.
```
luna node remove {Node Name}
```
8. Get a list of all Node Interfaces of a node.
```
luna node listinterface {Node Name}
```
9. Get a Detail of a  Interface of a node.
```
luna node showinterface {Node Name} {Interface Name}
```
10. Make change in a Node Interface.
```
luna node changeinterface {Node Name} {Interface Name} -N {Network Name} -I {IP Address} -M {MAC Address} -O {Interface Options}
```
11. Remove a Node Interface.
```
luna node removeinterface {Node Name} {Interface Name}
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
6. Change of all Node Secrets OR One Secret by name
```
luna secrets change node {Node Name} -s {Secret Name} -c {Content} -p {Path}
```
7. Change of all Group Secrets OR One Secret by name
```
luna secrets change group {Group Name} -s {Secret Name} -c {Content} -p {Path}
```
8. Clone a Node Secret.
```
luna secrets clone node {Node Name} {Secret Name} {New Secret Name} -c {Content} -p {Path}
```
9. Clone a Group Secret.
```
luna secrets clone group {Group Name} {Secret Name} {New Secret Name} -c {Content} -p {Path}
```
10. Delete a Node Secret.
```
luna secrets delete node {Node Name} {Secret Name}
```
11. Delete a Group Secret.
```
luna secrets delete group {Group Name} {Secret Name} 
```

## Commands Service
1. Perform action on DHCP Service
```
luna service dhcp {start/stop/restart/reload/status}
```
2. Perform action on DNS Service
```
luna service dns {start/stop/restart/reload/status}
```
3. Perform action on Luna 2 Daemon Service
```
luna service luna2 {start/stop/restart/reload/status}
```
## Commands Control
1. Check Node(s) power status
```
luna control power status {NodeName OR NodeList}
```
2. Power ON Node(s)
```
luna control power on {NodeName OR NodeList}
```
3. Power OFF Node(s)
```
luna control power off {NodeName OR NodeList}
```