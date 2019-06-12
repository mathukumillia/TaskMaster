#!/usr/bin/python3

from storage_manager import FileStorageManager
from list_manager import ListManager 
from task import Task 
from sys import stdin
from datetime import date, time

class App(object): 
    """
    The main task planner application object.
    """
    def __init__(self): 
        self.storage_manager = FileStorageManager("./storage")
        self.list_manager = ListManager(self.storage_manager.load_lists())
        self.task_map = self.storage_manager.load_tasks(self.list_manager)
        self.open_task_map = {}
        for task_id, task in self.task_map.items(): 
            if not task.completed: 
                self.open_task_map[task_id] = task

        self.EXIT_CMDS = ["quit", "exit", "q"]

    def run(self): 
        # for now, run a REPL loop that gives us a cmd line interface to the 
        # application 
        while True: 
            # print terminal cursor and retrieve cmd
            print(">>>", end=" ", flush=True)
            input_string = stdin.readline()

            # parse the input_string to get list of tokens
            tokens = self.tokenize_input(input_string) 
            cmd = tokens[0].lower()

            # creates a new task
            if cmd == "new": 
                # ensure we have the right number of arguments
                if len(tokens) != 5:
                    print("Invalid new command. The command takes the form: \n " 
                        + "new \"description\" date time list")
                    continue 

                # the first token is always the description  
                description = tokens[1]

                # parse the date 
                date = self.parse_date(tokens[2])
                if not date: 
                    print("Invalid date. Enter the date as MM/DD/YYYY")
                    continue

                # parse the time
                time = self.parse_time(tokens[3])
                if not time: 
                    print("Invalid time. Enter the time in 24 hour format")
                    continue

                # retrieve the list this task belongs to
                lst = tokens[4]

                self.add_task(description, date, time, lst)

            # removes tasks by ids
            elif cmd == "remove":
                for token in tokens[1:]:
                    task_id = None 
                    try: 
                        task_id = int(token)
                    except ValueError as e: 
                        print("{} is not a numeric id".format(token))
                        continue

                    if not self.remove_task(task_id):
                        print("Task {} does not exist".format(task_id))

            # view all of the existing tasks        
            elif cmd == "viewall":
                # if the user did not specify a particular list, then show all
                # tasks
                if len(tokens) == 1: 
                    for v in self.task_map.values(): 
                        print(v)
                        
                # otherwise, only show the tasks in that list
                else: 
                    sublist = filter(
                        lambda task: task.list in tokens[1:], 
                        self.task_map.values()
                    )
                    for v in sublist: 
                        print(v)

            # view all unfinished tasks
            elif cmd == "viewopen": 
                # if the user did not specify a particular list, then show all
                # tasks
                if len(tokens) == 1: 
                    for v in self.open_task_map.values(): 
                        print(v)
                        
                # otherwise, only show the tasks in that list
                else: 
                    sublist = filter(
                        lambda task: task.list in tokens[1:], 
                        self.open_task_map.values() 
                    )
                    for v in sublist: 
                        print(v)

            # add task lists
            elif cmd == "newlist": 
                for list_name in tokens[1:]:
                    if self.list_manager.add(list_name):
                        self.storage_manager.add_list(list_name)
                    else: 
                        print("List {} already exists".format(list_name))

            # remove task lists
            elif cmd == "removelist":
                for list_name in tokens[1:]:
                    # try to remove the list name
                    if self.list_manager.remove(list_name):
                        # if the list name was removed, remove tasks from task 
                        # map
                        tasks_to_remove = []
                        for task_id in self.task_map.keys(): 
                            task = self.task_map[task_id]
                            if task.list == list_name: 
                                tasks_to_remove.append(task_id)
                        for task_id in tasks_to_remove: 
                            del self.task_map[task_id]
                            if task_id in self.open_task_map.keys(): 
                                del self.open_task_map[task_id]

                        # remove list from storage
                        self.storage_manager.remove_list(list_name)

                    # otherwise, notify the user that the list doesn't exist
                    else: 
                        print("List {} does not exist".format(list_name))

            # generate and view the priority list 
            elif cmd == "prioritize":
                # sort the tasklist by closest deadline 
                tasklist = self.task_map.values()

            # complete tasks
            elif cmd == "complete":
                # complete each task the user wishes to complete 
                for token in tokens[1:]:
                    task_id = None 
                    try: 
                        task_id = int(token)
                    except ValueError as e: 
                        print("{} is not a numeric id".format(token))
                        continue
                    # if the task id does not correspond to a valid task, 
                    # report that to the user
                    if task_id not in self.task_map.keys(): 
                        print("Task {} is not a valid task.".format(task_id))
                    # if the task id has already been completed, tell user 
                    elif task_id not in self.open_task_map.keys(): 
                        print("Task {} has already been completed.".format(
                            task_id))
                    # otherwise, mark the task as completed
                    else: 
                        self.task_map[task_id].mark_completed()
                        del self.open_task_map[task_id]
                        self.storage_manager.mark_task_completed(task_id)


            # exit the task planner application
            elif cmd in self.EXIT_CMDS: 
                return

            # an invalid command was entered
            else: 
                print("Command not recognized!")

    def parse_date(self, date_token): 
        """
        Takes a string representation of a date (the date token) and converts
        it to a proper date object. Return None on parse failure.
        """
        date_elems = date_token.split("/")
        result = None
        if len(date_elems) != 3: 
            return None

        try: 
            date_elems = [int(elem) for elem in date_elems]
            result = date(date_elems[2], date_elems[0], date_elems[1])
        except Exception as e: 
            print("Got error parsing date: " + str(e))

        return result

    def parse_time(self, time_token): 
        """
        Takes a string representation of a time (the time token) and converts
        it to a proper date object.
        """
        time_elems = time_token.split(":")
        result = None 
        if len(time_elems) != 2: 
            return None 

        try: 
            time_elems = [int(elem) for elem in time_elems]
            result = time(time_elems[0], time_elems[1])
        except Exception as e: 
            print("Got error parsing time: " + str(e))

        return result

    def tokenize_input(self, string):
        """
        Takes a raw input string and returns a list of string tokens delimited
        by spaces, except in quoted sections.
        """
        tokens = []
        in_quotes = False
        curr_token = ""
        for char in string.strip(): 
            if char == "\"": 
                in_quotes = not in_quotes
            elif char == " " and not in_quotes and curr_token.strip(): 
                tokens.append(curr_token.strip())
                curr_token = ""
            else: 
                curr_token += char
        if curr_token.strip(): 
            tokens.append(curr_token.strip())
        return tokens

    def add_task(self, description, date, time, lst):
        # validate the list
        if not self.list_manager.validate(lst): 
            print("Invalid list name specified. Task creation failed.")
            return

        # create the task
        new_task = Task(
            None,
            description, 
            date, 
            time, 
            lst, 
        )

        # add the task to storage
        self.storage_manager.add_task(new_task)

        # storing task gives it a unique id that we can use to add to map
        self.task_map[new_task.get_id()] = new_task
        self.open_task_map[new_task.get_id()] = new_task
 
    def remove_task(self, task_id): 
        if task_id not in self.task_map.keys(): 
            return False
        del self.task_map[task_id] 
        if task_id in self.open_task_map.keys(): 
            del self.open_task_map[task_id]
        self.storage_manager.remove_task(task_id)
        return True

    def mark_task_completed(self, task_id): 
        self.task_map[task_id].mark_completed()

if __name__ == '__main__':
    app = App()
    app.run()