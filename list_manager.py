class ListManager(object): 
    """
    Creates, deletes, and validates lists of tasks.
    """
    def __init__(self, initial_list_set): 
        self.list_set = initial_list_set

    def add(self, lst): 
        if lst in self.list_set: 
            return False
        self.list_set.add(lst)
        return True

    def remove(self, lst):
        if lst not in self.list_set: 
            return False
        self.list_set.discard(lst)
        return True

    def validate(self, lst):
        return lst in self.list_set

    def get_default_list(self): 
        return "tasks"

