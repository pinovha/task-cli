import argparse
import os
import json

def add_task(args, status="in-progress"):
    task_data = read_json()
    if task_data:
        new_id = max(int(task_id) for task_id in task_data.keys()) + 1
    else:
        new_id = 1

    task_data[new_id] = {
        "description": args.description,
        "status": status 
    }
    
    write_json(task_data)

    print(""" 
    Zadanie "{}" zostało zapisane.
    Id: {}.
    """.format(args.description, new_id))

def del_task(args):
    task_id = args.task_id
    
    task_data = read_json()
   
    if not task_data:
        print("""
        Task list is empty.
        """)
        return

    if task_id in task_data:
        task_content = task_data[task_id]
        task_data.pop(task_id)
        write_json(task_data)
        print("""
        Task "{}", with ID: {} has been deleted.
        """.format(task_content["description"], task_id))
    else:
        print("""
        There is no task with given ID.
        """)

def list_tasks(args):
    task_data = read_json()
    if task_data:
        for task_id, task in task_data.items():
            print((""" 
        Id: {}
        Description: "{}" 
        Status: {} 
        """.format(task_id, task["description"], task["status"])))
    else:
        print("""
        There are no tasks.
        Add first by using: task-cli add "task" 
        """)
        
def read_json():
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        with open('data.json', 'r') as f:
            return json.load(f) 
    else:
        return {}

def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(prog="task-cli", description="Ten program służy do organizowania zadań.") 
    subparsers = parser.add_subparsers()

    # Dodawanie zadania
    add_parser = subparsers.add_parser("add", help="Dodaje nowe zadanie.")
    add_parser.add_argument("description", help="Treść zadania")
    add_parser.set_defaults(func=add_task)

    # Delete task
    del_parser = subparsers.add_parser("del", help="Deletes a specific task.")
    del_parser.add_argument("task_id", help="Id of the task you want to delete.")
    del_parser.set_defaults(func=del_task)

    # Wyświetlanie listy zadań
    list_parser = subparsers.add_parser("list", help="Wyświetla listę wszystkich zadań.")
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        
    



