# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024-2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import flet as ft
from core.db import Database
from core.models import Task
from core.views import TaskView


class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.new_task = ft.TextField(hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True)
        self.tasks = ft.Column()
        self.items_left = ft.Text("0 items left")
        self.filter = self.create_filter()

        self.controls = [
            ft.Row(
                [ft.Text(value="Todo List", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(text="Clear completed", on_click=self.clear_clicked),
                        ],
                    ),
                ],
            ),
        ]

    def create_filter(self):
        return ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

    def load_tasks(self):
        self.tasks.controls.clear()
        for row in self.db.get_all_tasks():
            task_uuid, task_name, completed, created_date, sort_order = row
            completed = bool(completed)
            task = Task(task_uuid, task_name, completed, created_date, sort_order)
            task_view = TaskView(
                task,
                self.task_status_change,
                self.task_delete,
                self.task_edit,
                self.task_move_up,
                self.task_move_down
            )
            self.tasks.controls.append(task_view)
        self.update()

    def add_clicked(self, e):
        if self.new_task.value:
            task_name = self.new_task.value
            task = Task(task_name=task_name)
            self.db.add_task(task.uuid, task_name)
            self.load_tasks()
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.db.update_task(task.uuid, task.name, task.completed)
        self.update()

    def task_delete(self, task):
        for task_view in self.tasks.controls:
            if task_view.task.uuid == task.uuid:
                self.db.delete_task(task.uuid)
                self.db.reorder_tasks()
                self.tasks.controls.remove(task_view)
                self.update()
                break

    def task_edit(self, task_view, new_name):
        self.db.update_task(task_view.task.uuid, new_name, task_view.task.completed)
        task_view.task.name = new_name
        task_view.task_text.value = new_name
        self.update()

    def task_move_up(self, task):
        self._move_task(task, -1)

    def task_move_down(self, task):
        self._move_task(task, 1)

    def _move_task(self, task, direction):
        current_index = None
        for i, task_view in enumerate(self.tasks.controls):
            if task_view.task.uuid == task.uuid:
                current_index = i
                break

        if current_index is None:
            return

        if (direction == -1 and current_index == 0) or (
                direction == 1 and current_index == len(self.tasks.controls) - 1):
            return

        swap_index = current_index + direction
        self.tasks.controls[current_index], self.tasks.controls[swap_index] = \
            self.tasks.controls[swap_index], self.tasks.controls[current_index]

        self._update_task_orders()
        self.update()

    def _update_task_orders(self):
        for index, task_view in enumerate(self.tasks.controls):
            self.db.update_task_order(task_view.task.uuid, index)

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task_view in self.tasks.controls[:]:
            if task_view.task.completed:
                self.task_delete(task_view.task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task_view in self.tasks.controls:
            task_view.visible = (
                    status == "all"
                    or (status == "active" and not task_view.task.completed)
                    or (status == "completed" and task_view.task.completed)
            )
            if not task_view.task.completed:
                count += 1
        self.items_left.value = f"{count} active task(s) left"
