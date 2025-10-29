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
    def __init__(self, task_uuid=None, task_name="", completed=False, created_date=None):
        self.uuid = task_uuid or str(uuid.uuid4())
        self.name = task_name
        self.completed = completed
        self.created_date = created_date or datetime.datetime.now()
