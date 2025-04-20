import argparse
import os
import json

def add_task(args, status="in-progress"):
    task_data = read_json()
    if task_data:
        new_id = max(task["id"] for task in task_data) + 1
    else:
        new_id = 1

    new_task = {
        "id": new_id,
        "description": args.task_content,
        "status": status 
    }
    
    task_data.append(new_task)
    write_json(task_data)

    print(""" 
    Zadanie {} zostało zapisane.
    Id: {}.
    """.format(args.task_content, new_id))

def list_tasks(args):
    task_data = read_json()
    for item in task_data:
        id, description, status = item.values()
        print(""" 
        Id: {}
        Opis: {}
        Status: {}
        """.format(id, description, status))
        
def read_json():
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        with open('data.json', 'r') as f:
            return json.load(f) 
    else:
        return []

def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(prog="task-cli", description="Ten program służy do organizowania zadań.") 
    subparsers = parser.add_subparsers()

    # Dodawanie zadania
    add_parser = subparsers.add_parser("add", help="Dodaje nowe zadanie.")
    add_parser.add_argument("task_content", help="Treść zadania")
    add_parser.set_defaults(func=add_task)

    # Wyświetlanie listy zadań
    add_parser = subparsers.add_parser("list", help="Wyświetla listę wszystkich zadań.")
    add_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        
    



