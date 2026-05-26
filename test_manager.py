"""
test_manager.py - Unit tests for TaskManager.
"""

import pytest
from todo.manager import TaskManager
from todo.models import Priority
from todo.storage import Storage


class InMemoryStorage(Storage):
    """A storage that never touches the filesystem — for testing."""

    def __init__(self):
        self._data = []

    def load(self):
        return list(self._data)

    def save(self, tasks):
        self._data = list(tasks)


@pytest.fixture
def manager():
    return TaskManager(storage=InMemoryStorage())


# ------------------------------------------------------------------ #
# add                                                                   #
# ------------------------------------------------------------------ #

def test_add_task(manager):
    task = manager.add("Buy groceries")
    assert task.id == 1
    assert task.title == "Buy groceries"


def test_add_assigns_incrementing_ids(manager):
    t1 = manager.add("First")
    t2 = manager.add("Second")
    assert t2.id == t1.id + 1


def test_add_empty_title_raises(manager):
    with pytest.raises(ValueError):
        manager.add("   ")


def test_add_with_priority(manager):
    task = manager.add("Urgent task", priority=Priority.HIGH)
    assert task.priority == Priority.HIGH


# ------------------------------------------------------------------ #
# complete                                                              #
# ------------------------------------------------------------------ #

def test_complete_task(manager):
    task = manager.add("Do laundry")
    manager.complete(task.id)
    assert manager.list_all()[0].is_done()


def test_complete_invalid_id_raises(manager):
    with pytest.raises(KeyError):
        manager.complete(999)


# ------------------------------------------------------------------ #
# delete                                                                #
# ------------------------------------------------------------------ #

def test_delete_task(manager):
    task = manager.add("Old task")
    manager.delete(task.id)
    assert manager.list_all() == []


def test_delete_invalid_id_raises(manager):
    with pytest.raises(KeyError):
        manager.delete(999)


# ------------------------------------------------------------------ #
# edit                                                                  #
# ------------------------------------------------------------------ #

def test_edit_task(manager):
    task = manager.add("Old title")
    updated = manager.edit(task.id, "New title")
    assert updated.title == "New title"


def test_edit_empty_title_raises(manager):
    task = manager.add("Something")
    with pytest.raises(ValueError):
        manager.edit(task.id, "")


# ------------------------------------------------------------------ #
# queries                                                               #
# ------------------------------------------------------------------ #

def test_list_pending(manager):
    t1 = manager.add("Task A")
    t2 = manager.add("Task B")
    manager.complete(t1.id)
    pending = manager.list_pending()
    assert len(pending) == 1
    assert pending[0].id == t2.id


def test_list_done(manager):
    t1 = manager.add("Task A")
    manager.add("Task B")
    manager.complete(t1.id)
    done = manager.list_done()
    assert len(done) == 1


def test_search(manager):
    manager.add("Buy apples")
    manager.add("Water the plants")
    results = manager.search("apple")
    assert len(results) == 1
    assert "apple" in results[0].title.lower()


def test_filter_by_priority(manager):
    manager.add("Low task", priority=Priority.LOW)
    manager.add("High task", priority=Priority.HIGH)
    highs = manager.filter_by_priority(Priority.HIGH)
    assert len(highs) == 1
    assert highs[0].priority == Priority.HIGH


def test_clear_done(manager):
    t1 = manager.add("Task 1")
    manager.add("Task 2")
    manager.complete(t1.id)
    removed = manager.clear_done()
    assert removed == 1
    assert len(manager.list_all()) == 1
