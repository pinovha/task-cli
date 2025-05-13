from argparse import ArgumentParser
import os
import json
import datetime
from typing import Dict, Any, List

DATA_FILE = "data.json"
STATUS_CHOICES = ["todo", "in-progress", "done"]
DATE_FORMAT = "%d/%m/%Y %H:%M"

class TaskManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.tasks = self._read_tasks()

    def _read_tasks(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
            with open(self.data_file, 'r') as f:
                return json.load(f) 
        else:
            return []

    def _save_tasks(self) -> None:
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=3)
    
    def _is_task_list_empty(self) -> bool:
        if not self.tasks:
            print("""
            Task list is empty.
            Add first by using: task-cli add "task"
            """)
            return True
        return False

    def add_task(self, description: str) -> None:
        if self.tasks:
            new_id: int = max(task["id"] for task in self.tasks) + 1
        else:
            new_id: int = 1

        self.tasks.append({
            "id": new_id,
            "description": description,
            "status": "todo", 
            "createdAt": datetime.datetime.now().strftime(DATE_FORMAT),
            "updatedAt": None 
        })
        self._save_tasks()
        print(f""" 
            Task "{description}" has been saved. With id = {new_id}.
            """)

    def del_task(self, task_id: int) -> None:
        if self._is_task_list_empty():
            return

        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                task_content = self.tasks.pop(i)
                self._save_tasks()
                print(f""" 
            Task "{task_content["description"]}" has been deleted.
            """)
                return

        print("""
            There is no task with given ID.
            """)

    def update_task(self, task_id: int, description: str) -> None:
        if self._is_task_list_empty():
            return

        for task in self.tasks:
            if task["id"] == task_id:
                old_description = task["description"]
                task["description"] = description
                task["updatedAt"] = datetime.datetime.now().strftime(DATE_FORMAT)
                self._save_tasks()
                print(f"""
            Task with ID: {task_id} has been updated!
            Old description: "{old_description}"
            New description: "{description}"
            """)
                return

        print("""
            There is no task with given ID.
            """)

    def list_tasks(self, status: str = None) -> None:
        if self._is_task_list_empty():
            return
        
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [task for task in self.tasks if task["status"] == status]
    
        if not filtered_tasks:
            print(f"""
            No tasks with status: {status}
            """)
            return

        for task in self.tasks: 
            updatedAt = task["updatedAt"] if task["updatedAt"] else "No changes recorded."
            
            print(f""" 
            Id: {task["id"]}
            Description: "{task["description"]}" 
            Status: {task["status"]}
            Created: {task["createdAt"]}
            Last Modified: {updatedAt}
            """)
            
    def mark_task(self, task_id: int, status: str) -> None:
        if self._is_task_list_empty():
            return

        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updatedAt"] = datetime.datetime.now().strftime(DATE_FORMAT)
                self._save_tasks()
                print(f"""
            Task "{task["description"]}" marked as {status}.
            """)
                return

        print(f"""
            Task with ID: {task_id} does not exist.
            """)

def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="task-cli", description="This program allows you to manage tasks.") 
    subparsers = parser.add_subparsers(help= "Available commands.")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add new task.")
    add_parser.add_argument("description", help="Task content.")
    add_parser.set_defaults(action="add")

    # Delete task
    del_parser = subparsers.add_parser("del", help="Delete a specific task.")
    del_parser.add_argument("id", type=int, help="Id of the task you want to delete.")
    del_parser.set_defaults(action="del")

    # Update task
    update_parser = subparsers.add_parser("update", help="Update a specific task.")
    update_parser.add_argument("id", type=int, help="Id of the task you want to upgrade.")
    update_parser.add_argument("description", help="New description of the task.")
    update_parser.set_defaults(action="update") 

    # Mark task
    mark_parser = subparsers.add_parser("mark", help="Marks the task.")
    mark_parser.add_argument("id", type=int, help="Id of the task you want to mark.")
    mark_parser.add_argument("status", choices=STATUS_CHOICES)
    mark_parser.set_defaults(action="mark")

    # List tasks
    list_parser = subparsers.add_parser("list", help="Display all tasks.")
    list_parser.add_argument("status", nargs="?", choices=STATUS_CHOICES, help="Filter tasks by status.")
    list_parser.set_defaults(action="list")
    
    return parser

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    task_manager = TaskManager()
    
    if hasattr(args, 'action'):
        if args.action == "add":
            task_manager.add_task(args.description)
        elif args.action == "del":
            task_manager.del_task(args.id)
        elif args.action == "update":
            task_manager.update_task(args.id, args.description)
        elif args.action == "mark":
            task_manager.mark_task(args.id, args.status)
        elif args.action == "list":
            task_manager.list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
