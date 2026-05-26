"""
test_models.py - Unit tests for the Task model.
"""

import pytest
from todo.models import Priority, Status, Task


def test_task_defaults():
    task = Task(title="Buy milk", id=1)
    assert task.title == "Buy milk"
    assert task.priority == Priority.MEDIUM
    assert task.status == Status.PENDING
    assert task.id == 1
    assert not task.is_done()


def test_task_complete():
    task = Task(title="Buy milk", id=1)
    task.complete()
    assert task.is_done()
    assert task.status == Status.DONE


def test_task_to_dict():
    task = Task(title="Read a book", priority=Priority.HIGH, id=2)
    d = task.to_dict()
    assert d["title"] == "Read a book"
    assert d["priority"] == "high"
    assert d["status"] == "pending"
    assert d["id"] == 2


def test_task_from_dict_roundtrip():
    task = Task(title="Exercise", priority=Priority.LOW, id=3)
    restored = Task.from_dict(task.to_dict())
    assert restored.title == task.title
    assert restored.priority == task.priority
    assert restored.status == task.status
    assert restored.id == task.id


def test_task_str_contains_title():
    task = Task(title="Walk the dog", id=5)
    assert "Walk the dog" in str(task)
