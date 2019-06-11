#!/usr/bin/python3

from storage_manager import FileStorageManager
from category_manager import CategoryManager 
from task import Task 
from sys import stdin
from datetime import date, time

class App(object): 
    """
    The main task planner application object.
    """
    def __init__(self): 
        self.storage_manager = FileStorageManager("./storage")
        self.category_manager = CategoryManager(self.storage_manager)
        self.task_map = self.storage_manager.load_tasks(self.category_manager)

    def run(self): 
        # for now, run a REPL loop that gives us a cmd line interface to the 
        # application 
        while True: 
            print(">>>", end=" ", flush=True)
            input_string = stdin.readline()
            elements = input_string.strip().split("\t")
            if elements[0] == "new":
                date_elems = [int(elem) for elem in elements[2].split("/")]
                time_elems = [int(elem) for elem in elements[3].split(":")]
                self.add_task(
                    elements[1], 
                    date(date_elems[2], date_elems[0], date_elems[1]), 
                    time(time_elems[0], time_elems[1]),
                    elements[4]
                )
            elif elements[0] == "view":
                for v in self.task_map.values(): 
                    print(v)
            elif elements[0] == "remove":
                self.remove_task(int(elements[1]))
            elif elements[0] == "exit" or elements[0] == "quit":
                return
            else: 
                print("Command not recognized!")

    def add_task(self, description, date, time, category):
        new_task = Task(
            description, 
            date, 
            time, 
            category, 
            self.category_manager, 
            self.storage_manager
        )
        self.task_map[new_task.get_id()] = new_task

    def remove_task(self, task_id): 
        del self.task_map[task_id] 
        self.storage_manager.remove_task(task_id)

    def mark_task_completed(self, task_id): 
        self.task_map[task_id].mark_completed()

if __name__ == '__main__':
    app = App()
    app.run()