import os.path
from task import Task

class StorageManager(object): 
    """
    An abstract class describing what a storage manager must be able to support. 
    Should not be instantiated.
    """
    def add_list(self, lst): 
        """
        Adds a list to the stored list of lists.
        """
        raise NotImplementedError

    def remove_list(self, lst): 
        """
        Removes a list from the stored list of lists.
        """
        raise NotImplementedError

    def load_lists(self):
        """
        Loads the list of lists into the application. 
        """
        raise NotImplementedError 

    def load_tasks(self): 
        """
        Loads all of the tasks into the application as a map of task ids to 
        tasks
        """
        raise NotImplementedError

    def add_task(self, task): 
        """
        Adds a task to the stored list of tasks.
        """
        raise NotImplementedError

    def remove_task(self, task_id): 
        """
        Removes a task from the stored list of tasks.
        """
        raise NotImplementedError

    def mark_task_completed(self, task_id): 
        """
        Marks a task as completed in storage.
        """
        raise NotImplementedError

class FileStorageManager(StorageManager): 
    """
    Uses raw text files as the backing store for this application. This is 
    probably not the best option, but it's good for small use cases and tests
    """
    def __init__(self, root): 
        self.root = root
        self.list_file = self.root + "/lists.txt"
        self.task_file = self.root + "/tasks.txt"
        self.num_tasks = 0

        # create all of the necessary storage files if they don't exist
        # list file
        if not os.path.exists(self.list_file): 
            with open(self.list_file, "w") as f:
                f.write("tasks\n");

        # task file
        if not os.path.exists(self.task_file): 
            with open(self.task_file, "w") as f: 
                pass

    def add_list(self, lst): 
        """
        Adds a list to the stored list of lists.
        """
        with open(self.list_file, "a") as f: 
            f.write(lst + "\n")

    def remove_list(self, lst): 
        """
        Removes a list from the stored list of lists, and then removes all 
        tasks associated with this list.
        """
        # remove list
        lines = None
        with open(self.list_file, "r") as f: 
            lines = f.readlines()
        with open(self.list_file, "w") as f: 
            for line in lines: 
                if line.strip() != lst: 
                    f.write(line)

        # remove associated tasks
        lines = None 
        with open(self.task_file, "r") as f: 
            lines = f.readlines()
        with open(self.task_file, "w") as f: 
            for line in lines: 
                elements = line.split("\t")
                if elements[4] != lst: 
                    f.write(line)


    def load_lists(self):
        """
        Loads the set of list names into the application. 
        """
        with open(self.list_file, "r") as f: 
            return set([line.strip() for line in f.readlines()])

    def load_tasks(self, list_manager): 
        """
        Loads all of the tasks into the application as a map of task ids to 
        tasks
        """
        task_map = {}
        with open(self.task_file, "r") as f: 
            for line in f: 
                elements = line.split("\t")
                task_map[int(elements[0])] = Task(
                    elements[0],
                    elements[1], 
                    elements[2], 
                    elements[3], 
                    elements[4],
                )
                if elements[5].strip() == "True":
                    task_map[int(elements[0])].mark_completed()
                if int(elements[0]) >= self.num_tasks:
                    self.num_tasks = int(elements[0]) + 1
        return task_map

    def add_task(self, task): 
        """
        Adds a task to the stored list of tasks.
        """
        task.set_id(self.num_tasks)
        with open(self.task_file, "a") as f: 
            f.write(str(task))
        self.num_tasks += 1

    def mark_task_completed(self, task_id): 
        """
        Marks a task as completed in storage.
        """
        lines = None
        with open(self.task_file, "r") as f: 
            lines = f.readlines()
        with open(self.task_file, "w") as f: 
            for line in lines: 
                elements = line.split("\t")
                if int(elements[0]) != task_id: 
                    f.write(line)
                else: 
                    f.write("\t".join(elements[:5]) + "\t" + str(True) + "\n")

    def remove_task(self, task_id): 
        """
        Removes a task from the stored list of tasks.
        """
        lines = None
        with open(self.task_file, "r") as f: 
            lines = f.readlines()
        with open(self.task_file, "w") as f: 
            for line in lines: 
                line_id = int(line.split("\t")[0])
                if line_id != task_id: 
                    f.write(line)       
