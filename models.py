"""
models.py - Task data model.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    PENDING = "pending"
    DONE = "done"


@dataclass
class Task:
    title: str
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    id: Optional[int] = None

    def complete(self) -> None:
        """Mark this task as done."""
        self.status = Status.DONE

    def is_done(self) -> bool:
        return self.status == Status.DONE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            created_at=data["created_at"],
        )

    def __str__(self) -> str:
        done_mark = "✓" if self.is_done() else "○"
        priority_map = {Priority.LOW: "↓", Priority.MEDIUM: "→", Priority.HIGH: "↑"}
        return f"[{done_mark}] #{self.id} {priority_map[self.priority]} {self.title}  ({self.created_at})"
