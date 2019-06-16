import sqlite3
from datetime import datetime, date, time

class DBStorageManager(object): 
    """
    Manages persistent storage in the task planner by reading/writing to/from 
    a sqlite database.
    """
    def __init__(self): 
        # establish database connection 
        self.conn = sqlite3.connect("taskplanner.db")
        self.cursor = self.conn.cursor()

        # the basal time stamp 
        self.base_time = datetime(2015, 1, 1)

        # enable foreign keys
        self.cursor.execute(
            """
            PRAGMA foreign_keys = ON;
            """
        )

        # create tables if they don't exist
        existing_tables = self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
            """
        )
        existing_tables = [tup[0] for tup in list(existing_tables)]
        if "lists" not in existing_tables: 
            self.cursor.execute(
                """
                CREATE TABLE lists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    priority INTEGER NOT NULL
                )
                """
            )
        if "tasks" not in existing_tables: 
            self.cursor.execute(
                """
                CREATE TABLE tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    sec_from_base INTEGER NOT NULL,
                    list_name TEXT NOT NULL,
                    completed INTEGER NOT NULL,
                    FOREIGN KEY (list_name) REFERENCES lists(name)
                )
                """
            )

    def create_task(self, description, date, time, list_name): 
        # compute the time delta from the basal time stamp 
        task_dt = datetime.combine(date, time)
        delta = task_dt - self.base_time
        try: 
            self.cursor.execute(
                """
                INSERT INTO tasks 
                (description, date, time, sec_from_base, list_name, completed)
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (description, str(date), str(time), delta.total_seconds(), 
                    list_name)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e: 
            print("Task creation failed: {} is not a valid list".format(
                list_name))

    def create_list(self, name, priority): 
        try: 
            self.cursor.execute(
                """
                INSERT INTO lists (name, priority)
                VALUES (?, ?)
                """,
                (name, priority)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e: 
            print("A list with the name {} already exists".format(name))

    def del_task(self, task_id): 
        self.cursor.execute(
            """
            DELETE FROM tasks WHERE id = ?
            """,
            (task_id, )
        )
        self.conn.commit()

    def del_list(self, lst_name): 
        # delete tasks on this list
        self.cursor.execute(
            "DELETE FROM tasks WHERE list_name = ?",
            (lst_name, )
        )
        # delete list
        self.cursor.execute(
            """
            DELETE FROM lists WHERE name = ?
            """,
            (lst_name, )
        )
        self.conn.commit()

    def complete(self, task_id): 
        self.cursor.execute(
            """
            UPDATE tasks SET completed = 1 WHERE id = ?
            """,
            (task_id, )
        )
        self.conn.commit()

    def viewtasks(self, list_name=None): 
        query = """ SELECT id, description, date, time, list_name 
                    FROM tasks WHERE completed = 0 """
        if list_name is not None: 
            query += "AND list_name = \"{}\"".format(list_name)
        tasks = self.cursor.execute(query)
        return list(tasks)

    def viewalltasks(self, list_name=None): 
        query = """ SELECT id, description, date, time, list_name, 
                    completed FROM tasks"""
        if list_name is not None: 
            query += " WHERE list_name = \"{}\"".format(list_name)
        tasks = self.cursor.execute(query)
        return list(tasks)

    def viewlists(self): 
        lists = self.cursor.execute(
            """
            SELECT * FROM lists
            """
        )
        return list(lists)

    def prioritize(self): 
        tasks = self.cursor.execute(
            """
            SELECT tasks.id, description, date, time, list_name, priority
            FROM tasks INNER JOIN lists ON lists.name = tasks.list_name 
            WHERE completed = 0 ORDER BY sec_from_base/priority ASC
            """
        )
        return list(tasks)
