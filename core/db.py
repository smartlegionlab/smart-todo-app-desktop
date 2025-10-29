# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024-2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='tasks.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                uuid TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                completed BOOLEAN NOT NULL,
                created_date TEXT NOT NULL,
                sort_order INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_task(self, uuid, name):
        created_date = datetime.now().isoformat()
        self.cursor.execute('SELECT COALESCE(MAX(sort_order), 0) FROM tasks')
        max_order = self.cursor.fetchone()[0]
        sort_order = max_order + 1

        self.cursor.execute(
            'INSERT INTO tasks (uuid, name, completed, created_date, sort_order) VALUES (?, ?, ?, ?, ?)',
            (uuid, name, False, created_date, sort_order)
        )
        self.conn.commit()

    def update_task(self, uuid, name, completed):
        self.cursor.execute(
            'UPDATE tasks SET name = ?, completed = ? WHERE uuid = ?',
            (name, int(completed), uuid)
        )
        self.conn.commit()

    def update_task_order(self, uuid, sort_order):
        self.cursor.execute(
            'UPDATE tasks SET sort_order = ? WHERE uuid = ?',
            (sort_order, uuid)
        )
        self.conn.commit()

    def delete_task(self, uuid):
        self.cursor.execute('DELETE FROM tasks WHERE uuid = ?', (uuid,))
        self.conn.commit()

    def get_all_tasks(self):
        self.cursor.execute('SELECT uuid, name, completed, created_date, sort_order FROM tasks ORDER BY sort_order')
        return self.cursor.fetchall()

    def reorder_tasks(self):
        self.cursor.execute('SELECT uuid FROM tasks ORDER BY sort_order')
        tasks = self.cursor.fetchall()
        for index, (uuid,) in enumerate(tasks):
            self.cursor.execute('UPDATE tasks SET sort_order = ? WHERE uuid = ?', (index, uuid))
        self.conn.commit()

    def close(self):
        self.conn.close()
