"""Shared backend for the Task Manager.

Both the Tkinter and the PyQt interfaces use this module, so tasks created
in one interface are visible in the other (they share the same JSON file).
"""

import json
import os
from dataclasses import dataclass, asdict

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

PRIORITIES = ("Low", "Medium", "High")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "Medium"
    done: bool = False


class TaskManager:
    """Stores tasks and saves them to a JSON file."""

    def __init__(self, data_file=DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.tasks = []
        self.load()

    def load(self):
        if not os.path.exists(self.data_file):
            self.tasks = []
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.tasks = [Task(**item) for item in json.load(f)]
        except (json.JSONDecodeError, TypeError):
            self.tasks = []

    def save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2)

    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def add_task(self, title, priority="Medium"):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}.")
        task = Task(id=self._next_id(), title=title, priority=priority)
        self.tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}.")

    def toggle_done(self, task_id):
        task = self.get_task(task_id)
        task.done = not task.done
        self.save()
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.tasks.remove(task)
        self.save()

    def clear_completed(self):
        removed = len([t for t in self.tasks if t.done])
        self.tasks = [t for t in self.tasks if not t.done]
        self.save()
        return removed

    def stats(self):
        done = sum(1 for t in self.tasks if t.done)
        return {"total": len(self.tasks), "done": done, "pending": len(self.tasks) - done}
