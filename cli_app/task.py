#!/usr/bin/env python3
"""Task Manager CLI - Command-line interface for task management"""
import argparse
import sys
from typing import Optional
from task_manager import TaskManager


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def format_task(task: dict, show_id: bool = True) -> str:
    """Format a task for display"""
    status = "✓" if task["completed"] else "○"
    priority_colors = {
        "high": Colors.FAIL,
        "medium": Colors.WARNING,
        "low": Colors.OKBLUE
    }
    
    priority = task.get("priority", "medium")
    color = priority_colors.get(priority, Colors.ENDC)
    
    task_str = f"{color}[{status}]"
    if show_id:
        task_str += f" #{task['id']}"
    task_str += f" {task['description']}"
    task_str += f" ({priority}){Colors.ENDC}"
    
    return task_str


def cmd_add(args, tm: TaskManager) -> None:
    """Add a new task"""
    task = tm.add_task(args.description, args.priority)
    print(f"{Colors.OKGREEN}✓ Task added:{Colors.ENDC} {format_task(task)}")


def cmd_list(args, tm: TaskManager) -> None:
    """List tasks"""
    tasks = tm.list_tasks(show_completed=args.all, priority=args.priority)
    
    if not tasks:
        print(f"{Colors.WARNING}No tasks found.{Colors.ENDC}")
        return
    
    header = "All Tasks" if args.all else "Pending Tasks"
    if args.priority:
        header += f" (Priority: {args.priority})"
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}{header}{Colors.ENDC}")
    print("=" * 50)
    
    for task in tasks:
        print(format_task(task))
    
    print()


def cmd_complete(args, tm: TaskManager) -> None:
    """Mark a task as completed"""
    task = tm.complete_task(args.id)
    if task:
        print(f"{Colors.OKGREEN}✓ Task completed:{Colors.ENDC} {task['description']}")
    else:
        print(f"{Colors.FAIL}✗ Task #{args.id} not found.{Colors.ENDC}")
        sys.exit(1)


def cmd_delete(args, tm: TaskManager) -> None:
    """Delete a task"""
    task = tm.get_task(args.id)
    if task:
        if tm.delete_task(args.id):
            print(f"{Colors.OKGREEN}✓ Task deleted:{Colors.ENDC} {task['description']}")
        else:
            print(f"{Colors.FAIL}✗ Failed to delete task #{args.id}.{Colors.ENDC}")
            sys.exit(1)
    else:
        print(f"{Colors.FAIL}✗ Task #{args.id} not found.{Colors.ENDC}")
        sys.exit(1)


def cmd_stats(args, tm: TaskManager) -> None:
    """Show task statistics"""
    stats = tm.get_statistics()
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}Task Statistics{Colors.ENDC}")
    print("=" * 50)
    print(f"Total tasks:     {stats['total']}")
    print(f"{Colors.OKGREEN}Completed:       {stats['completed']}{Colors.ENDC}")
    print(f"{Colors.WARNING}Pending:         {stats['pending']}{Colors.ENDC}")
    print("\nPending by priority:")
    print(f"  {Colors.FAIL}High:   {stats['by_priority']['high']}{Colors.ENDC}")
    print(f"  {Colors.WARNING}Medium: {stats['by_priority']['medium']}{Colors.ENDC}")
    print(f"  {Colors.OKBLUE}Low:    {stats['by_priority']['low']}{Colors.ENDC}")
    print()


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  task add "Buy groceries" -p high
  task list
  task list --all
  task complete 1
  task delete 2
  task stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")
    parser_add.add_argument("-p", "--priority", choices=["high", "medium", "low"],
                           default="medium", help="Task priority (default: medium)")
    
    # List command
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("-a", "--all", action="store_true",
                            help="Show all tasks including completed")
    parser_list.add_argument("-p", "--priority", choices=["high", "medium", "low"],
                            help="Filter by priority")
    
    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("id", type=int, help="Task ID")
    
    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID")
    
    # Stats command
    parser_stats = subparsers.add_parser("stats", help="Show task statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize TaskManager
    tm = TaskManager()
    
    # Execute command
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "delete": cmd_delete,
        "stats": cmd_stats
    }
    
    commands[args.command](args, tm)


if __name__ == "__main__":
    main()
