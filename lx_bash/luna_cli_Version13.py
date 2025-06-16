import argparse
import argcomplete
from luna.utils.completion import (
    node_name_completer, group_name_completer, osimage_name_completer,
    network_name_completer, empty_completer
)

def main():
    parser = argparse.ArgumentParser(description="Luna2 CLI")
    subparsers = parser.add_subparsers(dest="resource")

    # ---- NODE ----
    node_parser = subparsers.add_parser("node", help="Node operations")
    node_subparsers = node_parser.add_subparsers(dest="action")

    node_list = node_subparsers.add_parser("list", help="List Nodes")

    node_show = node_subparsers.add_parser("show", help="Show Node")
    node_show.add_argument("name", help="Node name").completer = node_name_completer

    node_remove = node_subparsers.add_parser("remove", help="Remove Node")
    node_remove.add_argument("name", help="Node name").completer = node_name_completer

    node_clone = node_subparsers.add_parser("clone", help="Clone Node")
    node_clone.add_argument("name", help="Node to clone").completer = node_name_completer
    node_clone.add_argument("newnodename", help="New Node name").completer = empty_completer

    node_rename = node_subparsers.add_parser("rename", help="Rename Node")
    node_rename.add_argument("name", help="Current Node name").completer = node_name_completer
    node_rename.add_argument("newnodename", help="New Node name").completer = empty_completer

    node_add = node_subparsers.add_parser("add", help="Add Node")
    node_add.add_argument("--network", help="Network name", default=None).completer = network_name_completer
    # ... add other node_add arguments as needed ...

    # ---- GROUP ----
    group_parser = subparsers.add_parser("group", help="Group operations")
    group_subparsers = group_parser.add_subparsers(dest="action")

    group_list = group_subparsers.add_parser("list", help="List Groups")

    group_show = group_subparsers.add_parser("show", help="Show Group")
    group_show.add_argument("name", help="Group name").completer = group_name_completer

    group_remove = group_subparsers.add_parser("remove", help="Remove Group")
    group_remove.add_argument("name", help="Group name").completer = group_name_completer

    group_clone = group_subparsers.add_parser("clone", help="Clone Group")
    group_clone.add_argument("name", help="Group to clone").completer = group_name_completer
    group_clone.add_argument("newgroupname", help="New Group name").completer = empty_completer

    group_rename = group_subparsers.add_parser("rename", help="Rename Group")
    group_rename.add_argument("name", help="Current Group name").completer = group_name_completer
    group_rename.add_argument("newgroupname", help="New Group name").completer = empty_completer

    group_add = group_subparsers.add_parser("add", help="Add Group")
    group_add.add_argument("--network", help="Network name", default=None).completer = network_name_completer
    # ... add other group_add arguments as needed ...

    # ---- OSIMAGE ----
    osimage_parser = subparsers.add_parser("osimage", help="OSImage operations")
    osimage_subparsers = osimage_parser.add_subparsers(dest="action")

    osimage_list = osimage_subparsers.add_parser("list", help="List OSImages")

    osimage_show = osimage_subparsers.add_parser("show", help="Show OSImage")
    osimage_show.add_argument("name", help="OSImage name").completer = osimage_name_completer

    osimage_remove = osimage_subparsers.add_parser("remove", help="Remove OSImage")
    osimage_remove.add_argument("name", help="OSImage name").completer = osimage_name_completer

    osimage_clone = osimage_subparsers.add_parser("clone", help="Clone OSImage")
    osimage_clone.add_argument("name", help="OSImage to clone").completer = osimage_name_completer
    osimage_clone.add_argument("newosimage", help="New OSImage name").completer = empty_completer

    osimage_rename = osimage_subparsers.add_parser("rename", help="Rename OSImage")
    osimage_rename.add_argument("name", help="Current OSImage name").completer = osimage_name_completer
    osimage_rename.add_argument("newosimage", help="New OSImage name").completer = empty_completer

    osimage_pack = osimage_subparsers.add_parser("pack", help="Pack OSImage")
    osimage_pack.add_argument("name", help="OSImage name").completer = osimage_name_completer

    osimage_add = osimage_subparsers.add_parser("add", help="Add OSImage")
    # ... add other osimage_add arguments as needed ...

    # ---- Enable argcomplete ----
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    # ... main Luna logic ...

if __name__ == "__main__":
    main()