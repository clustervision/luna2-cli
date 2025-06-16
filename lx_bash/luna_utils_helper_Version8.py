class Helper:
    # ... existing code ...

    @staticmethod
    def get_all_names(table):
        """
        Return a sorted list of all names for the given table (e.g. 'node', 'group', 'osimage', 'network').
        """
        from luna.utils.rest import Rest
        try:
            get_list = Rest().get_data(table)
            if get_list.status_code == 200:
                content = get_list.content
                if content and "config" in content and table in content["config"]:
                    return sorted(content["config"][table].keys())
        except Exception:
            pass
        return []