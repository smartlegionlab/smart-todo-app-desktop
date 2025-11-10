# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024-2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import datetime
import uuid


class Task:
    def __init__(self, task_uuid=None, task_name="", completed=False, created_date=None, sort_order=0,priority="Medium"):
        self.uuid = task_uuid or str(uuid.uuid4())
        self.name = task_name
        self.completed = completed
        self.created_date = created_date or datetime.datetime.now()
        self.sort_order = sort_order
        self.priority = priority

        # Optional helper: to make saving/loading to JSON or database easier

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "task_name": self.name,
            "completed": self.completed,
            "created_date": self.created_date.isoformat(),
            "sort_order": self.sort_order,
            "priority": self.priority,  # include priority
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task_uuid=data.get("uuid"),
            task_name=data.get("task_name", ""),
            completed=data.get("completed", False),
            created_date=datetime.datetime.fromisoformat(data["created_date"])
            if "created_date" in data
            else None,
            sort_order=data.get("sort_order", 0),
            priority=data.get("priority", "Medium"),  # default if missing
        )