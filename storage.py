"""
storage.py - Handles reading and writing tasks to a JSON file.
"""

import json
import os
from typing import List

from todo.models import Task

DEFAULT_PATH = os.path.join(os.path.expanduser("~"), ".todo_data.json")


class Storage:
    def __init__(self, filepath: str = DEFAULT_PATH) -> None:
        self.filepath = filepath

    def load(self) -> List[Task]:
        """Load all tasks from the JSON file."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task.from_dict(item) for item in data]

    def save(self, tasks: List[Task]) -> None:
        """Persist all tasks to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)
