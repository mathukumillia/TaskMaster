from datetime import datetime

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

    def get_list(self): 
        return self.list

    def __str__(self): 
        return (str(self.id) + "\t" + self.description + "\t" + str(self.date) + "\t" +
            str(self.time) + "\t" + str(self.list) + "\t" + str(self.completed) + "\n")

    def __eq__(self, other):
        return (
            (self.date == other.time) and 
            (self.time == other.time) and 
            (self.list.get_priority() == other.get_priority())
        ) 

    def __lt__(self, other): 
        mytime = datetime.combine(self.date, self.time)
        othertime = datetime.combine(self.date, self.time)

        myweight = (mytime - datetime.today()).total_seconds()/self.list.get_priority()
        otherweight = (othertime - datetime.today()).total_seconds()/other.list.get_priority()

        if myweight < otherweight: 
            return True
        return False
