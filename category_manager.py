class CategoryManager(object): 
    """
    Creates, deletes, and validates categories of tasks.
    """
    def __init__(self, storage_manager): 
        self.storage_manager = storage_manager
        self.load()

    def add(self, category): 
        self.category_set.add(category)
        self.storage_manager.add_category(category)

    def remove(self, category):
        self.category_set.discard(category)
        self.storage_manager.remove_category(category)

    def validate(self, category):
        return category in self.category_set

    def load(self): 
        self.category_set = self.storage_manager.load_categories()

    def get_default_category(self): 
        return "tasks"

