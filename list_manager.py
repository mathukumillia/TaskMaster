class ListManager(object): 
    """
    Creates, deletes, and validates lists of tasks.
    """
    def __init__(self, storage_manager): 
        self.storage_manager = storage_manager
        self.load()

    def add(self, list): 
        self.list_set.add(list)
        self.storage_manager.add_list(list)

    def remove(self, list):
        self.list_set.discard(list)
        self.storage_manager.remove_list(list)

    def validate(self, lst):
        return lst in self.list_set

    def load(self): 
        self.list_set = self.storage_manager.load_lists()

    def get_default_list(self): 
        return "tasks"

