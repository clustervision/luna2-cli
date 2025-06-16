from luna.utils.helper import Helper

def node_name_completer(prefix, parsed_args, **kwargs):
    return [n for n in Helper.get_all_names("node") if n.startswith(prefix)]

def group_name_completer(prefix, parsed_args, **kwargs):
    return [n for n in Helper.get_all_names("group") if n.startswith(prefix)]

def osimage_name_completer(prefix, parsed_args, **kwargs):
    return [n for n in Helper.get_all_names("osimage") if n.startswith(prefix)]

def network_name_completer(prefix, parsed_args, **kwargs):
    return [n for n in Helper.get_all_names("network") if n.startswith(prefix)]

def empty_completer(prefix, parsed_args, **kwargs):
    return []