import datetime

class Task(object): 
    """
    Represents a single task.
    """
    def __init__(self, task_id, description, date, time, lst): 
        self.description = description
        self.date = date
        self.time = time 
        self.completed = False
        self.list = lst
        self.id = task_id

    def get_id(self):
        return self.id

    def set_id(self, task_id): 
        self.id = task_id 

    def mark_completed(self): 
        self.completed = True

    def __str__(self): 
        return (str(self.id) + "\t" + self.description + "\t" + str(self.date) + "\t" +
            str(self.time) + "\t" + self.list + "\t" + str(self.completed) + "\n")



