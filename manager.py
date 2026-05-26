"""
manager.py - Business logic for managing tasks.
"""

from typing import List, Optional

from todo.models import Priority, Status, Task
from todo.storage import Storage


class TaskManager:
    def __init__(self, storage: Optional[Storage] = None) -> None:
        self.storage = storage or Storage()
        self._tasks: List[Task] = self.storage.load()
        self._next_id: int = max((t.id for t in self._tasks), default=0) + 1

    # ------------------------------------------------------------------ #
    # CRUD                                                                  #
    # ------------------------------------------------------------------ #

    def add(self, title: str, priority: Priority = Priority.MEDIUM) -> Task:
        """Create and persist a new task."""
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = Task(title=title, priority=priority, id=self._next_id)
        self._next_id += 1
        self._tasks.append(task)
        self._persist()
        return task

    def complete(self, task_id: int) -> Task:
        """Mark a task as done."""
        task = self._get_by_id(task_id)
        task.complete()
        self._persist()
        return task

    def delete(self, task_id: int) -> Task:
        """Remove a task permanently."""
        task = self._get_by_id(task_id)
        self._tasks.remove(task)
        self._persist()
        return task

    def edit(self, task_id: int, title: str) -> Task:
        """Edit the title of an existing task."""
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = self._get_by_id(task_id)
        task.title = title
        self._persist()
        return task

    # ------------------------------------------------------------------ #
    # Queries                                                               #
    # ------------------------------------------------------------------ #

    def list_all(self) -> List[Task]:
        return list(self._tasks)

    def list_pending(self) -> List[Task]:
        return [t for t in self._tasks if not t.is_done()]

    def list_done(self) -> List[Task]:
        return [t for t in self._tasks if t.is_done()]

    def filter_by_priority(self, priority: Priority) -> List[Task]:
        return [t for t in self._tasks if t.priority == priority]

    def search(self, keyword: str) -> List[Task]:
        keyword = keyword.lower()
        return [t for t in self._tasks if keyword in t.title.lower()]

    def clear_done(self) -> int:
        """Delete all completed tasks. Returns the count removed."""
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if not t.is_done()]
        self._persist()
        return before - len(self._tasks)

    # ------------------------------------------------------------------ #
    # Helpers                                                               #
    # ------------------------------------------------------------------ #

    def _get_by_id(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task found with id {task_id}.")

    def _persist(self) -> None:
        self.storage.save(self._tasks)
