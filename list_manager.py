class ListManager(object): 
    """
    Creates, deletes, and validates lists of tasks.
    """
    def __init__(self, initial_lists): 
        # lists are stored as a map of name to list objects
        self.list_map = initial_lists

    def add(self, lst): 
        if lst.get_name() in self.list_map.keys(): 
            return False
        self.list_map[lst.get_name()] = lst
        return True

    def remove(self, lst):
        if lst.get_name() not in self.list_map.keys():
            return False
        del self.list_map[lst.get_name()]
        return True

    def validate(self, lst_name):
        return lst_name in self.list_map.keys()

    def get_lst(self, lst_name): 
        return self.list_map[lst_name]


class List(object): 
    """
    Encapsulates the name and priority multiplier of a list.
    """
    def __init__(self, name, priority): 
        self.name = name
        self.priority = priority

    def get_name(self): 
        return self.name

    def get_priority(self): 
        return self.priority

    def __str__(self): 
        return self.name