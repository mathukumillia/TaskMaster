#!/usr/bin/python3

from storage_manager import DBStorageManager
from sys import stdin

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
                self.storage_manager.add_task(tokens[1], tokens[2], tokens[3], 
                    tokens[4])
            elif cmd in self.NEW_LIST_CMDS: 
                self.storage_manager.create_list(tokens[1], tokens[2])
            elif cmd in self.DEL_TASK_CMDS: 
                self.storage_manager.del_task(tokens[1])
            elif cmd in self.DEL_LIST_CMDS: 
                self.storage_manager.del_list(tokens[1])
            elif cmd in self.COMPLETE_CMDS: 
                self.storage_manager.complete(tokens[1])
            elif cmd in self.PRIORITIZE_CMDS: 
                tasks = self.storage_manager.prioritize()
                for task in tasks: 
                    print(task)
            elif cmd in self.VIEW_TASKS_CMDS: 
                tasks = self.storage_manager.viewtasks()
                for task in tasks: 
                    print(task)
            elif cmd in self.VIEW_ALLTASKS_CMDS: 
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