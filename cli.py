"""
cli.py - Command-line interface for the To-Do app.
"""

import argparse
import sys

from todo.manager import TaskManager
from todo.models import Priority


# ------------------------------------------------------------------ #
# Helpers                                                               #
# ------------------------------------------------------------------ #

PRIORITY_COLORS = {
    "high": "\033[91m",   # red
    "medium": "\033[93m", # yellow
    "low": "\033[94m",    # blue
}
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
DIM = "\033[2m"


def _colored_task(task) -> str:
    color = PRIORITY_COLORS.get(task.priority.value, "")
    done_mark = f"{GREEN}✓{RESET}" if task.is_done() else "○"
    priority_icon = {"low": "↓", "medium": "→", "high": "↑"}[task.priority.value]
    title = f"{DIM}{task.title}{RESET}" if task.is_done() else task.title
    return (
        f"  [{done_mark}] {BOLD}#{task.id}{RESET}  "
        f"{color}{priority_icon} {task.priority.value:<6}{RESET}  "
        f"{title}  {DIM}({task.created_at}){RESET}"
    )


def _print_tasks(tasks) -> None:
    if not tasks:
        print(f"  {DIM}No tasks found.{RESET}")
        return
    for task in tasks:
        print(_colored_task(task))


def _print_header(text: str) -> None:
    width = 60
    print(f"\n{BOLD}{'─' * width}{RESET}")
    print(f"{BOLD}  {text}{RESET}")
    print(f"{BOLD}{'─' * width}{RESET}")


# ------------------------------------------------------------------ #
# Command handlers                                                      #
# ------------------------------------------------------------------ #

def cmd_add(manager: TaskManager, args: argparse.Namespace) -> None:
    priority = Priority(args.priority)
    task = manager.add(args.title, priority=priority)
    print(f"\n{GREEN}✓ Task added:{RESET} #{task.id} — {task.title} [{task.priority.value}]")


def cmd_list(manager: TaskManager, args: argparse.Namespace) -> None:
    _print_header("All Tasks")
    _print_tasks(manager.list_all())
    total = len(manager.list_all())
    done = len(manager.list_done())
    print(f"\n  {DIM}Total: {total}  |  Done: {done}  |  Pending: {total - done}{RESET}\n")


def cmd_pending(manager: TaskManager, _args) -> None:
    _print_header("Pending Tasks")
    _print_tasks(manager.list_pending())
    print()


def cmd_done_list(manager: TaskManager, _args) -> None:
    _print_header("Completed Tasks")
    _print_tasks(manager.list_done())
    print()


def cmd_complete(manager: TaskManager, args: argparse.Namespace) -> None:
    try:
        task = manager.complete(args.id)
        print(f"\n{GREEN}✓ Marked as done:{RESET} #{task.id} — {task.title}\n")
    except KeyError as e:
        print(f"\n  Error: {e}\n", file=sys.stderr)
        sys.exit(1)


def cmd_delete(manager: TaskManager, args: argparse.Namespace) -> None:
    try:
        task = manager.delete(args.id)
        print(f"\n  Deleted: #{task.id} — {task.title}\n")
    except KeyError as e:
        print(f"\n  Error: {e}\n", file=sys.stderr)
        sys.exit(1)


def cmd_edit(manager: TaskManager, args: argparse.Namespace) -> None:
    try:
        task = manager.edit(args.id, args.title)
        print(f"\n{GREEN}✓ Task updated:{RESET} #{task.id} — {task.title}\n")
    except (KeyError, ValueError) as e:
        print(f"\n  Error: {e}\n", file=sys.stderr)
        sys.exit(1)


def cmd_search(manager: TaskManager, args: argparse.Namespace) -> None:
    results = manager.search(args.keyword)
    _print_header(f'Search: "{args.keyword}"')
    _print_tasks(results)
    print()


def cmd_filter(manager: TaskManager, args: argparse.Namespace) -> None:
    priority = Priority(args.priority)
    results = manager.filter_by_priority(priority)
    _print_header(f"Priority: {args.priority}")
    _print_tasks(results)
    print()


def cmd_clear_done(manager: TaskManager, _args) -> None:
    removed = manager.clear_done()
    print(f"\n  Removed {removed} completed task(s).\n")


# ------------------------------------------------------------------ #
# Argument parser                                                       #
# ------------------------------------------------------------------ #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple yet complete command-line To-Do List app.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)",
    )

    # list
    sub.add_parser("list", help="List all tasks")

    # pending
    sub.add_parser("pending", help="List only pending tasks")

    # done (list)
    sub.add_parser("done-list", help="List completed tasks")

    # complete
    p_complete = sub.add_parser("complete", help="Mark a task as done")
    p_complete.add_argument("id", type=int, help="Task ID")

    # delete
    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID")

    # edit
    p_edit = sub.add_parser("edit", help="Edit a task title")
    p_edit.add_argument("id", type=int, help="Task ID")
    p_edit.add_argument("title", help="New task title")

    # search
    p_search = sub.add_parser("search", help="Search tasks by keyword")
    p_search.add_argument("keyword", help="Keyword to search")

    # filter
    p_filter = sub.add_parser("filter", help="Filter tasks by priority")
    p_filter.add_argument("priority", choices=["low", "medium", "high"])

    # clear-done
    sub.add_parser("clear-done", help="Remove all completed tasks")

    return parser


# ------------------------------------------------------------------ #
# Entry-point                                                           #
# ------------------------------------------------------------------ #

COMMAND_MAP = {
    "add": cmd_add,
    "list": cmd_list,
    "pending": cmd_pending,
    "done-list": cmd_done_list,
    "complete": cmd_complete,
    "delete": cmd_delete,
    "edit": cmd_edit,
    "search": cmd_search,
    "filter": cmd_filter,
    "clear-done": cmd_clear_done,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager()
    COMMAND_MAP[args.command](manager, args)


if __name__ == "__main__":
    main()
