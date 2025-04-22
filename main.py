import argparse
import os
import json
import datetime

def add_task(args, status="todo"):
    task_data = read_json()
    if task_data:
        new_id = max(int(task_id) for task_id in task_data.keys()) + 1
    else:
        new_id = 1

    current_date = datetime.datetime.now().strftime("%d/%m/%Y")

    task_data[new_id] = {
        "description": args.description,
        "status": status, 
        "createdAt": current_date,
        "updatedAt": None
    }
    
    write_json(task_data)

    print(""" 
        Zadanie "{}" zostało zapisane.
        Id: {}.
        """.format(args.description, new_id))

def del_task(args):
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

        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        task["updatedAt"] = current_date
        
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
    task_data = read_json()
        
    if is_empty(task_data):
        return
  
    for task_id, task in task_data.items():
        updatedAt = task["updatedAt"]
        if updatedAt == None:
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
    status = args.status

    if task_id in task_data:
        task = task_data[task_id]
        if status == "in-progress" or status == "done":
            task["status"] = status

            current_date = datetime.datetime.now().strftime("%d/%m/%Y")
            task["updatedAt"] = current_date
 
            write_json(task_data)

            print("""
        Task "{}" marked as {}.
            """.format(task["description"], status))
        else:
            print("""
        Wrong mark, please use:
        "in-progress" or "done"
            """)
    else:
        print("""
        Task with ID: {} does not exist.
        """.format(task_id))

def read_json():
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        with open('data.json', 'r') as f:
            return json.load(f) 
    else:
        return {}

def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def create_parser():
    parser = argparse.ArgumentParser(prog="task", description="This program allows you to manage tasks.") 
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
    mark_parser.add_argument("status", help="Choose status: in-progress, done.")
    mark_parser.add_argument("id", help="Id of the task you want to mark.")
    mark_parser.set_defaults(func=mark_task)

    # Wyświetlanie listy zadań
    list_parser = subparsers.add_parser("list", help="Wyświetla listę wszystkich zadań.")
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
