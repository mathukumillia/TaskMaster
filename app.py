#!/usr/bin/python3

from storage_manager import DBStorageManager
from sys import stdin
from datetime import date, time

class App(object): 
    """
    The main task planner application object.
    """
    def __init__(self): 
        """
        Initializes the storage manager and the set of valid commands.
        """
        self.storage_manager = DBStorageManager()

        self.EXIT_CMDS = ["quit", "exit", "q"]
        self.NEW_TASK_CMDS = ["newtask", "nt"]
        self.NEW_LIST_CMDS = ["newlist", "nl"]
        self.DEL_TASK_CMDS = ["deltask", "dt"]
        self.DEL_LIST_CMDS = ["dellist", "dl"]
        self.COMPLETE_CMDS = ["complete", "c"]
        self.PRIORITIZE_CMDS = ["prioritize", "p"]
        self.VIEW_TASKS_CMDS = ["viewtasks", "vt"]
        self.VIEW_ALLTASKS_CMDS = ["viewalltasks", "vat"]
        self.VIEW_LISTS_CMDS = ["viewlists", "vl"]

    def run(self):
        """
        Runs a REPL loop that reads commands and runs them.
        """
        while True: 
            # print terminal cursor
            print(">>>", end = " ", flush=True)
            # retrieve input
            input_string = stdin.readline()

            # parse the input string to get list of tokens
            tokens = self.tokenize_input(input_string)
            cmd = tokens[0].lower()

            # run the cmd
            if cmd in self.NEW_TASK_CMDS: 
                if len(tokens) != 5: 
                    print("Usage: nt description date time list_name")
                    continue
                if self.convert_date(tokens[2]) is None: 
                    continue
                elif self.convert_time(tokens[3]) is None:
                    continue
                self.storage_manager.create_task(tokens[1], tokens[2], tokens[3], 
                    tokens[4])
            elif cmd in self.NEW_LIST_CMDS: 
                if len(tokens) != 3: 
                    print("Usage: nl name priority")
                    continue
                if self._safe_int(tokens[2]) is None: 
                    continue
                self.storage_manager.create_list(tokens[1], tokens[2])
            elif cmd in self.DEL_TASK_CMDS: 
                if len(tokens) != 2: 
                    print("Usage: dt task_id")
                    continue 
                self.storage_manager.del_task(tokens[1])
            elif cmd in self.DEL_LIST_CMDS: 
                if len(tokens) != 2: 
                    print("Usage: dl list_name")
                    continue 
                self.storage_manager.del_list(tokens[1])
            elif cmd in self.COMPLETE_CMDS: 
                if len(tokens) != 2: 
                    print("Usage: c task_id")
                    continue 
                self.storage_manager.complete(tokens[1])
            elif cmd in self.PRIORITIZE_CMDS: 
                tasks = self.storage_manager.viewtasks()
                tasks = [(task_id, description, self.convert_date(d), 
                    self.convert_time(t), list_name) 
                    for task_id, description, d, t, list_name in tasks]
                tasks = sorted(tasks, key=lambda x: (x[2], x[3]))
                for task in tasks: 
                    print(task)
            elif cmd in self.VIEW_TASKS_CMDS: 
                tasks = []
                if len(tokens) == 2: 
                    tasks = self.storage_manager.viewtasks(tokens[1])
                else: 
                    tasks = self.storage_manager.viewtasks()
                for task in tasks: 
                    print(task)
            elif cmd in self.VIEW_ALLTASKS_CMDS: 
                tasks = []
                if len(tokens) == 2: 
                    tasks = self.storage_manager.viewalltasks(tokens[1])
                else: 
                    tasks = self.storage_manager.viewalltasks()
                for task in tasks: 
                    print(task)
            elif cmd in self.VIEW_LISTS_CMDS: 
                lists = self.storage_manager.viewlists()
                for lst in lists: 
                    print(lst)
            elif cmd in self.EXIT_CMDS: 
                return 
            else: 
                print("Invalid command entered!")


    # ====================== Helper methods ===================================
    def _safe_int(self, num):
        """
        Converts the given string into an integer. Returns None if num is not a
        valid integer.
        """
        integer = None
        try: 
            integer = int(num)
        except ValueError as e: 
            print("{} is not a valid number".format(num))
        return integer

    def convert_date(self, date_token): 
        """
        Ensures that dates take the form MM/DD/YYYY because the db does not.
        """
        # ensure each part of date is numeric
        date_elems = date_token.split("/")
        if len(date_elems) != 3:
            print("Date must be specified as MM/DD/YYYY")
            return None

        month = self._safe_int(date_elems[0])
        if not month:
            return None
        day = self._safe_int(date_elems[1])
        if not day: 
            return None
        year = self._safe_int(date_elems[2])
        if year is None: 
            return None

        # try to create a date object
        try: 
            return date(year, month, day)
        except ValueError as e: 
            print("{} is not a valid date".format(date_token))
            return None

    def convert_time(self, time_token): 
        """
        Ensures that times take the form HH:MM because the db does not.
        """
        # ensure each part of time is numeric
        time_elems = time_token.split(":")
        if len(time_elems) != 2:
            print("Time must be specified in 24 hour format: HH:MM")
            return None

        hour = self._safe_int(time_elems[0])
        if hour is None: 
            return None
        minutes = self._safe_int(time_elems[1])
        if minutes is None: 
            return None

        # try to create a time object
        try: 
            return time(hour, minutes)
        except ValueError as e: 
            print("{} is not a valid time".format(time_token))
            return None

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

if __name__ == '__main__':
    tasks_app = App()
    tasks_app.run()