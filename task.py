import datetime

class Task(object): 
    """
    Represents a single task.
    """
    def __init__(self, description, date, time, category, category_manager, storage_manager, store=True, task_id=None): 
        self.description = description
        self.date = date
        self.time = time 
        self.completed = False

        self.category_manager = category_manager
        self.storage_manager = storage_manager

        if not category: 
            self.category = self.category_manager.get_default_category()
        elif self.category_manager.validate(category): 
            self.category = category
        else: 
            raise TypeError

        self.id = None
        if store: 
            self.storage_manager.add_task(self)
        else: 
            self.id = int(task_id)

    def mark_completed(self): 
        self.completed = True
        self.storage_manager.mark_task_completed(self.id)

    def get_id(self): 
        return self.id

    def set_id(self, task_id): 
        self.id = task_id

    def __str__(self): 
        return (str(self.id) + "\t" + self.description + "\t" + str(self.date) + "\t" +
            str(self.time) + "\t" + self.category + "\t" + str(self.completed) + "\n")



