import os.path
from task import Task

class StorageManager(object): 
    """
    An abstract class describing what a storage manager must be able to support. 
    Should not be instantiated.
    """
    def add_category(self, category): 
        """
        Adds a category to the stored list of categories.
        """
        raise NotImplementedError

    def remove_category(self, category): 
        """
        Removes a category from the stored list of categories.
        """
        raise NotImplementedError

    def load_categories(self):
        """
        Loads the list of categories into the application. This list should 
        always include a default "tasks" category.
        """
        raise NotImplementedError 

    def load_tasks(self): 
        """
        Loads all of the uncompleted tasks into the application as a map of 
        task ids to tasks
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
        self.category_file = self.root + "/categories.txt"
        self.task_file = self.root + "/tasks.txt"
        self.num_tasks = 0

        # create all of the necessary storage files if they don't exist
        # category file
        if not os.path.exists(self.category_file): 
            with open(self.category_file, "w") as f:
                f.write("tasks\n");

        # task file
        if not os.path.exists(self.task_file): 
            with open(self.task_file, "w") as f: 
                pass

    def add_category(self, category): 
        """
        Adds a category to the stored list of categories.
        """
        with open(self.category_file, "w+") as f: 
            f.write(category + "\n")

    def remove_category(self, category): 
        """
        Removes a category from the stored list of categories.
        """
        lines = None
        with open(self.category_file, "w+") as f: 
            lines = f.readlines()
        with open(self.category_file, "w") as f: 
            for line in lines: 
                if line.strip() != category: 
                    f.write(line)


    def load_categories(self):
        """
        Loads the list of categories into the application. This list should 
        always include a default "tasks" category.
        """
        with open(self.category_file, "r") as f: 
            return [line.strip() for line in f.readlines()]

    def load_tasks(self, category_manager): 
        """
        Loads all of the uncompleted tasks into the application as a map of 
        task ids to tasks
        """
        task_map = {}
        with open(self.task_file, "r") as f: 
            for line in f: 
                elements = line.split("\t")
                if bool(elements[5]):
                    task_map[int(elements[0])] = Task(elements[1], elements[2], elements[3], elements[4],
                        category_manager, self, store=False, task_id=int(elements[0]))
                if int(elements[0]) > self.num_tasks:
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
        with open(self.task_file, "w+") as f: 
            lines = f.readlines()
        with open(self.task_file, "w") as f: 
            for line in lines: 
                elements = line.split("\t")
                if int(elements[0]) != task_id: 
                    f.write(line)
                else: 
                    f.write("\t".join(elements[:6]) + "\t" + str(True))

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
