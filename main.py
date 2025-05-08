import argparse
import os
import json
import datetime
from typing import Dict

def add_task(args: argparse.Namespace) -> None:
    description: str = args.description
    task_data = read_json()

    if task_data:
        new_id: str = str(max(int(task_id) for task_id in task_data.keys()) + 1)
    else:
        new_id: str = "1"

    task_data[new_id] = {
        "description": description,
        "status": "todo", 
        "createdAt": datetime.datetime.now().strftime("%d/%m/%Y"),
        "updatedAt": ""
    }
    
    write_json(task_data)

    print(""" 
        Task "{}" has been saved. With id = {}.
        """.format(description, new_id))

def del_task(args: argparse.Namespace) -> None:
    task_id = args.id
    task_data = read_json()
   
    if is_empty(task_data):
        return

    task_content = task_data.pop(task_id, None)

    if task_content:
        write_json(task_data)
        print("""
        Task "{}", with ID: {} has been deleted.
        """.format(task_content["description"], task_id))
    else:
        print("""
        There is no task with given ID.
        """)

def update_task(args):
    task_id = args.id
    task_data = read_json()

    if is_empty(task_data):
        return

    if task_id in task_data:
        description = args.description
        task = task_data[task_id]

        old_description = task["description"]
        task["description"] = description

        task["updatedAt"] = datetime.datetime.now().strftime("%d/%m/%Y")
        
        write_json(task_data)

        print("""
        Task with ID: {} has been updated!
        Old description: "{}"
        New description: "{}"
        """.format(task_id, old_description, task["description"]))
    else:
        print("""
        There is no task with given ID.
        """)

def is_empty(data):
    if not data:
        print("""
        Task list is empty.
        Add first by using: task-cli add "task"
        """)
        return True
    return False

def list_tasks(args):
    status = args.status
    task_data = read_json()
        
    if is_empty(task_data):
        return
    
    if args.status:
        task_data = {task_id: task for task_id, task in task_data.items() if task["status"] == status}
  
    if not task_data:
        print("""
        No tasks with status: {}
        """.format(status))

    for task_id, task in task_data.items():
        updatedAt = task["updatedAt"]
        if updatedAt == "":
            updatedAt = "No changes recorded."
        
        print((""" 
        Id: {}
        Description: "{}" 
        Status: {}
        Created: {}
        Last Modified: {}
        """.format(task_id, task["description"], task["status"], task["createdAt"], updatedAt)))
        
def mark_task(args):
    task_data = read_json()

    if is_empty(task_data):
        return

    task_id = args.id

    if task_id not in task_data:
        print("""
        Task with ID: {} does not exist.
        """.format(task_id))
        return

    status = args.status
    
    task = task_data[task_id]
    task["status"] = status
    task["updatedAt"] = datetime.datetime.now().strftime("%d/%m/%Y")
    
    write_json(task_data)

    print("""
        Task "{}" marked as {}.
        """.format(task["description"], status))

def read_json() -> Dict[str, Dict[str, str]]:
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        with open('data.json', 'r') as f:
            return json.load(f) 
    else:
        return {}

def write_json(data) -> None:
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def create_parser():
    parser = argparse.ArgumentParser(prog="task-cli", description="This program allows you to manage tasks.") 
    subparsers = parser.add_subparsers()

    # Add task
    add_parser = subparsers.add_parser("add", help="Add new task.")
    add_parser.add_argument("description", help="Task content.")
    add_parser.set_defaults(func=add_task)

    # Delete task
    del_parser = subparsers.add_parser("del", help="Delete a specific task.")
    del_parser.add_argument("id", help="Id of the task you want to delete.")
    del_parser.set_defaults(func=del_task)

    # Update task
    update_parser = subparsers.add_parser("update", help="Update a specific task.")
    update_parser.add_argument("id", help="Id of the task you want to upgrade.")
    update_parser.add_argument("description", help="New description of the task.")
    update_parser.set_defaults(func=update_task) 

    # Mark task
    mark_parser = subparsers.add_parser("mark", help="Marks the task.")
    mark_parser.add_argument("status", choices=["in-progress", "done"], help="Choose status: in-progress, done.")
    mark_parser.add_argument("id", help="Id of the task you want to mark.")
    mark_parser.set_defaults(func=mark_task)

    # List tasks
    list_parser = subparsers.add_parser("list", help="Display all tasks.")
    list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter tasks by status.")
    list_parser.set_defaults(func=list_tasks)
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
