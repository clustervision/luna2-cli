# luna2-cli

`luna` is the command-line interface of Luna, the provisioning and cluster management system
of TrinityX. It talks to the Luna daemon (luna2-daemon) over its REST API and covers
everything the daemon manages: the cluster, networks, OS images, groups, nodes, hardware,
secrets, profiles and access control. It runs on the controllers and can also be installed
on any host that can reach the daemon.

## Features

- One command for the whole cluster, with the same verbs on every object: `list`, `show`,
  `add`, `change`, `clone`, `rename`, `remove`, and `member` where an object is used by others.
- Tables for people and raw JSON (`-R`, `--raw`) for scripts.
- Bash completion for commands, options and object names.
- Node lists in hostlist notation, for example `node[001-032]`, for power and other actions.
- Cluster, network, group and node configuration, including interfaces, IPv4 and IPv6
  addressing, DNS entries, static routes, disk layouts and network mounts.
- OS image management: pack, cancel a pack, kernel selection, tags and certificate updates;
  `osgrab` and `ospush` to capture a node into an image or push an image onto nodes.
- Hardware management: power, system event log, chassis identify, one-time boot into BIOS
  setup, Redfish actions, BIOS configurations, the firmware catalogue and node hardware
  inventory.
- Secrets at cluster, group and node level, and profiles assigned to groups and nodes with
  per-node delivery status.
- Role-based access control (RBAC): per-person login, users, user groups with roles,
  directory group mapping, and object permissions changed with `chmod`, `chgrp` and `chown`.
- Boot progress of the cluster, daemon status and queue, and control of the DHCP and DNS
  services.

## Commands

Run `luna <command> --help` or `luna <command> <action> --help` for the options of each action.

| Command | Actions | Purpose |
|---|---|---|
| `cluster` | `show`, `change`, `showmounts`, `addmount`, `removemount` | Cluster settings and cluster-wide network mounts |
| `network` | `list`, `show`, `add`, `change`, `rename`, `remove`, `reserve`, `ipinfo`, `nextip`, `dns`, `route` | Networks, IP address lookup, DNS entries and the static-route catalogue |
| `osimage` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `member`, `pack`, `cancel`, `kernel`, `tag`, `updatecerts` | OS images, packing, kernels and tags |
| `group` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `member`, `ospush`, `biospush`, `firmwarepush`, interface actions, `showdisklayout`, `showmounts`, `addmount`, `removemount`, `assignprofile`, `unassignprofile` | Groups, their interfaces, mounts and profiles, and actions on all their nodes |
| `node` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `osgrab`, `ospush`, `biosgrab`, `biospush`, `firmwarepush`, interface actions, `listinventory`, `showinventory`, `refreshinventory`, `setupredfish`, `showdisklayout`, `showmounts`, `addmount`, `removemount`, `assignprofile`, `unassignprofile` | Nodes, their interfaces, inventory, mounts and profiles |
| `switch` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, interface actions | Switches and their ports |
| `otherdev` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove` | Other network devices |
| `cloud` | `list`, `show`, `add`, `change`, `rename`, `remove` | Cloud providers |
| `bmcsetup` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `member` | BMC setups |
| `redfishsetup` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `member`, `addaccount`, `changeaccount`, `removeaccount` | Redfish setups and the accounts they create on the BMC |
| `biosconfig` | `list`, `show`, `change`, `clone`, `rename`, `remove`, `status` | BIOS configurations grabbed from nodes, and what every node holds |
| `firmwarecatalog` | `list`, `show`, `add`, `change`, `rename`, `remove`, `status` | Firmware catalogue and the outcome of firmware updates |
| `secrets` | `list`, `show`, `add`, `change`, `clone`, `remove`, each for `cluster`, `group` or `node` | Secrets per level |
| `profile` | `list`, `show`, `add`, `change`, `clone`, `rename`, `remove`, `member`, `status`, `addfile`, `changefile`, `removefile` | Profiles, their files and delivery status |
| `control` | `power` (`on`, `off`, `reset`, `status`), `sel` (`list`, `clear`), `chassis` (`identify`, `noidentify`), `nextboot` (`bios`, `status`, `clear`), `redfish` (`upload`, `setting`) | Hardware actions on one node or a node list |
| `boot` | `status` | Where the cluster is in a (re)boot cycle |
| `service` | `dhcp` or `dns`, with `start`, `stop`, `restart`, `reload`, `status` | Control of the DHCP and DNS services |
| `monitor` | `status`, `queue` | Daemon status and queue |
| `user` | `list`, `show`, `add`, `change`, `rename`, `remove`, `access` | Users, and what a user holds |
| `usergroup` | `list`, `show`, `add`, `change`, `rename`, `remove`, `access`, `member`, `addmember`, `removemember`, `map`, `addmap`, `removemap` | User groups, members with their roles, and directory group mapping |
| `access` | `login`, `logout`, `whoami`, `chmod`, `chgrp`, `chown`, `addusergroup`, `removeusergroup`, `addowner`, `removeowner` | Logging in, and the permissions on an object |

The interface actions are `listinterface`, `showinterface`, `changeinterface`,
`removeinterface` and `renameinterface`.

Common options: `-h`, `--help` on every level, `-R`, `--raw` for JSON output, `-v`,
`--verbose` for debugging and `-V`, `--version` for the version.

## Access control (RBAC)

Luna uses role-based access control (RBAC). Every object has owners, user groups and an
access mode, shown the way `ls -l` shows a file:

```
luna access login                         # log in as yourself
luna access whoami                        # who the daemon takes you for
luna access chmod node node001 rwxr-x---  # or octal: 750
luna access chgrp group compute +admins   # add a user group; -name removes, a list replaces
luna access chown osimage compute alice
```

`luna access login` writes `~/.luna/luna.ini` and keeps a personal token beside it, so each
person works under their own identity. `luna access logout` removes both.

## Configuration

`luna` reads its settings from `~/.luna/luna.ini` after `luna access login`, and otherwise from
`/trinity/local/luna/cli/config/luna.ini`. It uses the `[API]` section: the daemon endpoint
and protocol, certificate verification and the account to log in with.

**On a TrinityX cluster, the TrinityX installer writes a fresh
`/trinity/local/luna/cli/config/luna.ini` on every run and replaces whatever the file
contained.** Change settings through the TrinityX configuration, not in the file on the
controller. The CLI does not depend on TrinityX: it works with any Luna daemon it can reach,
and `luna.ini` is then maintained by hand. A personal `~/.luna/luna.ini` is not touched by
the installer.

The log is written to `/var/log/luna/luna2-cli.log`, or to `~/.luna/luna2-cli.log` when that
file is not writable.

---


Luna 2 CLI is a part of the Luna 2 Project.<br />
Luna 2 CLI is a Command Line Interface, And used to interact with Luna 2 Daemon over Microservices.<br />
It will use REST API's to communicate to the daemon.<br />
Luna2 CLI's Prime location is Cluster, but also can be installed on the nodes.<br />

## Installation

pip install luna2-cli

The package is not on PyPI. Build it from this repository with
`pip wheel --no-build-isolation .`, or take it from the TrinityX package repository. On a
TrinityX controller the TrinityX installer installs it.

## Usage
* -h or --help can be run anywhere to see the required parameters.
* -R or --raw will be useful to see the data in json while using list or show arguments.
* -V or --version will be useful to see the current version of Luna.
* -v or --verbose will be useful for debugging purpose.
* Log File location -> /var/log/luna/luna2-cli.log


## Commands Cluster
1. Detailed view of cluster and controllers
```
luna cluster show
```
2. Make change in Cluster information.
```
luna cluster change -n {Cluster Name} -u {Cluster User} -T {NTP Server IP} -C {Create Node On Demand} -ns {Name Server IP} -fs {Forward Server IP} -t {Technical Contact} -p {Provision Method} -f {Provision Fallback} -s {Security} --debug {Debug Mode}
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
luna network add {Network Name} -N {Network} -g {Gateway} -S {Name Server IP} -T {NTP Server IP} -D {DHCP} -b {DHCP Range Start} -e {DHCP Range End} -qc {Comment}
```
4. Make change in network information.
```
luna network change {Network Name} -N {Network} -g {Gateway} -S {Name Server IP} -T {NTP Server IP} -D {DHCP} -b {DHCP Range Start} -e {DHCP Range End} -qc {Comment}
```
5. Rename a network.
```
luna network rename {Network Name} {New Network Name}
```
6. Remove a network.
```
luna network remove {Network Name}
```
7. Get a Information of an IP, such as it is free or taken.
```
luna network ipinfo {Network Name} {IP Address}
```
8. Get next available IP on the network.
```
luna network nextip {Network Name}
```

## Commands OSImage
1. List of all osimages
```
luna osimage list
```
2. Detailed view of a os images
```
luna osimage show {OSImage Name}
```
3. Add a os images.
```
luna osimage add {OSImage Name} -qG {Grab Filesystems} -qE {Grab Exclude} -r {InitRD File} -f {Kernel File} -m {Kernel Modules} -qo {Kernel Options} -k {Kernel Version} -p {Path Of Image} -i {Image File} -d {Distribution} -l {OS Release} -qc {Comment}
```
4. Make change in a os images.
```
luna osimage change {OSImage Name} -qG {Grab Filesystems} -qE {Grab Exclude} -r {InitRD File} -f {Kernel File} -m {Kernel Modules} -qo {Kernel Options} -k {Kernel Version} -p {Path Of Image} -i {Image File} -d {Distribution} -l {OS Release} -qc {Comment}
```
5. Clone a os images.
```
luna osimage clone {OSImage Name} {New OSImage Name} -qG {Grab Filesystems} -qE {Grab Exclude} -r {InitRD File} -f {Kernel File} -m {Kernel Modules} -qo {Kernel Options} -k {Kernel Version} -p {Path Of Image} -i {Image File} -d {Distribution} -l {OS Release} -qc {Comment}
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
luna osimage kernel {OSImage Name} -r {InitRD File} -f {Kernel File} -k {Kernel Version}
```
10. OSImage used by nodes.
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
luna bmcsetup add {BMC Setup Name} -i {User ID} -u {Username} -p {Password} -n {Network Channel} -m {Management Channel} -U {Unmanaged BMC Users} -C {Cipher Suite} -qc {Comment}
```
4. Make change in BMC Setup.
```
luna bmcsetup change {BMC Setup Name} -i {User ID} -u {Username} -p {Password} -n {Network Channel} -m {Management Channel} -U {Unmanaged BMC Users} -C {Cipher Suite} -qc {Comment}
```
5. Clone a BMC Setup.
```
luna bmcsetup clone {BMC Setup Name} {New BMC Setup Name} -i {User ID} -u {Username} -p {Password} -n {Network Channel} -m {Management Channel} -U {Unmanaged BMC Users} -C {Cipher Suite} -qc {Comment}
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
luna switch add {Switch Name} -N {Network} -I {IP Address} -M {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -qc {Comment}
```
4. Make change in a Switch.
```
luna switch change {Switch Name} -N {Network} -I {IP Address} -M {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -qc {Comment}
```
5. Clone a Switch.
```
luna switch clone {Switch Name} {New Switch Name} -N {Network} -I {IP Address} -M {MAC Address} -r {Read Community} -w {Write Community} -o {OID} -qc {Comment}
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
luna otherdev add {Other Device Name} -N {Network} -I {IP Address} -M {Mac Address} -qc {Comment}
```
4. Make change in a Other Device.
```
luna otherdev change {Other Device Name} -N {Network} -I {IP Address} -M {Mac Address} -qc {Comment}
```
5. Clone a Other Device.
```
luna otherdev clone {Other Device Name} {New Other Device Name} -N {Network} -I {IP Address} -M {Mac Address} -qc {Comment}
```
6. Rename a Other Device.
```
luna otherdev rename {Other Device Name} {New Other Device Name}
```
7. Remove a Other Device.
```
luna otherdev remove {Other Device Name}
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
luna group add {Group Name} -e {BMC Setup} -b {BMC Setup Name} -d {Domain Name} -o {OSImage Name} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -n {Network Boot} -m {Boot Menu} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -U {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -qo {Interface Options} -qc {Comment}
```
4. Make change in a Group.
```
luna group change {Group Name} -e {BMC Setup} -b {BMC Setup Name} -d {Domain Name} -o {OSImage Name} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -n {Network Boot} -m {Boot Menu} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -U {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -qo {Interface Options} -qc {Comment}
```
5. Clone a Group.
```
luna group clone {Group Name} {New Group Name} -e {BMC Setup} -b {BMC Setup Name} -d {Domain Name} -o {OSImage Name} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -n {Network Boot} -m {Boot Menu} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -U {Unmanaged BMC Users} -if {Interface Name} -N {Interface Network Name} -qo {Interface Options} -qc {Comment}
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
luna group changeinterface {Group Name} {Interface Name} -N {Network Name} -qO {Interface Options}
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
luna node add {Node Name} -g {Group Name} -o {OSImage Name} -e {BMC Setup} -b {BMC Setup Name} --switch {Switch Name} --switchport {Switch Port} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -n {Network Boot} -m {Boot Menu} --status {Status} --tpm_uuid {TPM UUID} --tpm_pubkey {TPM Public Key} --tpm_sha256 {TPM SHA256} -U {Unmanaged BMC Users} -qc {Comment} -if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -qo {Interface Options}
```
4. Make change in a Node.
```
luna node change {Node Name} -g {Group Name} -o {OSImage Name} -e {BMC Setup} -b {BMC Setup Name} --switch {Switch Name} --switchport {Switch Port} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -n {Network Boot} -m {Boot Menu} --status {Status} --tpm_uuid {TPM UUID} --tpm_pubkey {TPM Public Key} --tpm_sha256 {TPM SHA256} -U {Unmanaged BMC Users} -qc {Comment} -if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -qo {Interface Options}
```
5. Clone a Node.
```
luna node clone {Node Name} {New Node Name} -g {Group Name} -o {OSImage Name} -e {BMC Setup} -b {BMC Setup Name} --switch {Switch Name} --switchport {Switch Port} -qpre {Pre Script} -qpart {Part Script} -qpost {Post Script} -i {Provision Interface} -p {Provision Method} -f {Provision Fallback} -n {Network Boot} -m {Boot Menu} --status {Status} --tpm_uuid {TPM UUID} --tpm_pubkey {TPM Public Key} --tpm_sha256 {TPM SHA256} -U {Unmanaged BMC Users} -qc {Comment} -if {Interface Name} -N {Interface Network Name} -I {Interface IP Address} -M {Interface MAC Address} -qo {Interface Options}
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
luna node changeinterface {Node Name} {Interface Name} -N {Network Name} -I {IP Address} -M {MAC Address} -qO {Interface Options}
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
5. Details of a Group Secret
```
luna secrets show group {Group Name} {Secret Name}
```
6. Change a Node Secret
```
luna secrets change node {Node Name} {Secret Name} -qc {Content} -p {Path}
```
7. Change a Group Secret
```
luna secrets change group {Group Name} {Secret Name} -qc {Content} -p {Path}
```
8. Clone a Node Secret.
```
luna secrets clone node {Node Name} {Secret Name} {New Secret Name} -qc {Content} -p {Path}
```
9. Clone a Group Secret.
```
luna secrets clone group {Group Name} {Secret Name} {New Secret Name} -qc {Content} -p {Path}
```
10. Remove a Node Secret.
```
luna secrets remove node {Node Name} {Secret Name}
```
11. Remove a Group Secret.
```
luna secrets remove group {Group Name} {Secret Name}
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
4. Reset Node(s)
```
luna control power reset {NodeName OR NodeList}
```

## Daemon HTTP 500 errors

Every HTTP request, including login and status followers, stops with exit status 1
on a daemon 500. When run on the controller with permission to read its daemon
log, the CLI shows a compact exception and the innermost file, line and function:

```text
HTTP ERROR :: 500 Server Error
    TypeError: unsupported operand type(s) for +: 'NoneType' and 'list' (routes/config_cluster.py:60, in config_cluster)
```

The CLI reads the daemon's LOGGER/LOGFILE setting from
`/trinity/local/luna/daemon/config/luna.ini`, falling back to
`/var/log/luna/luna2-daemon.log` when that setting cannot be read. It does not
modify daemon configuration or require changes to the daemon API.

Only bytes written during the HTTP call are inspected, with a limit of 128 KiB.
Matching uses Flask's logged path and HTTP method. Existing logs have no unique
request ID, so correlation is best effort: simultaneous failures for the same
path and method cannot be attributed exactly without daemon support. Multiple
matches are rejected. Redirects, proxies, remote controllers, unreadable or
rotated logs, missing tracebacks and unsupported trace formats retain the HTTP
500 message and suggest checking the controller daemon log. The CLI does not
open an SSH connection or change log permissions. Full traces and source lines
remain in the daemon log.

## Contributing

Please read the [contribution guidelines](Guidelines.rst) before submitting changes, including the legal terms that apply to all contributions.
