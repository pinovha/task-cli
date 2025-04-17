import argparse

def add_task(args):
    print("Dodano zadanie.")

def main():
    parser = argparse.ArgumentParser(prog="task-cli", description="Ten program służy do organizowania zadań.") 
    subparsers = parser.add_subparsers()

    # Dodawanie zadania
    add_parser = subparsers.add_parser("add", help="Dodaje nowe zadanie.")
    add_parser.add_argument("task_content", help="Treść zadania")
    add_parser.set_defaults(func=add_task)


    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        




