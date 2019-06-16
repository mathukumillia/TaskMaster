# TaskMaster

TaskMaster is a basic task planning application with a command line interface.

## Dependencies 

1. python3
2. sqlite3
3. sqlite3 module for python3

## Running TaskMaster

You may need to add executable permissions to app.py by running: 
```
chmod +x app.py
```
Once app.py is executable, you can run TaskMaster by executing: 
```
./app.py
```

## Basic Commands

### Creating a List

TaskMaster organizes tasks into lists; you need to create a list before you can
assign any tasks to it. To do so, you can run: 
```
>> nl name priority
```
The priority is a number used to rank tasks when organizing your daily todo 
list. You can view this as an indicator of the relative importance of the tasks 
on that list.

### Creating a Task

Each task has a description, date (MM/DD/YYYY), 24 hour time (HH:MM), and list 
associated with it. To create one, you can run:
```
>> nt description date time list_name
```
Tasks are assigned IDs automatically by sqlite.

### Complete a Task

Tasks are initialized as unfinished. Once you've completed a task, you can run:
```
>> c task_id
```

### Deleting a Task

In general, you probably don't want to delete tasks, because you'll want to 
keep track of your progress. If, however, you really need to delete a task, 
you can run: 
```
>> dt task_id
```

### Deleting a List

Deleting an entire list deletes all of the tasks on that list as well: 
```
>> dl list_name
```

### Prioritizing

The prioritizing feature searches through all of the tasks on all of your lists
and sorts them by nearest completion date and priority. It essentially gives 
you a todo list ranked by deadline and weighted by priority. To generate this 
todo list, just run: 
```
>> p
```

### Viewing Tasks

You can view tasks in several different ways. If you want to see all tasks, 
completed and uncompleted, you can run: 
```
>> vat
```
If you want to see all tasks, completed and uncompleted, from a particular list,
you can run: 
```
>> vat list_name
```
You can see all uncompleted tasks by running: 
```
>> vt
```
Once again, you can filter out uncompleted tasks from a particular list by 
running: 
``` 
>> vt list_name
```

### Viewing Lists

Finally, you can see all of the lists you have by running: 
```
>> vl
```