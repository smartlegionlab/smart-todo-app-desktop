# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
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
            task_uuid, task_name, completed = row
            completed = bool(completed)
            task = Task(task_uuid, task_name, completed)
            task_view = TaskView(task, self.task_status_change, self.task_delete, self.task_edit)
            self.tasks.controls.append(task_view)
        self.update()

    def add_clicked(self, e):
        if self.new_task.value:
            task_name = self.new_task.value
            task = Task(task_name=task_name)
            self.db.add_task(task.uuid, task_name)
            task_view = TaskView(task, self.task_status_change, self.task_delete, self.task_edit)
            self.tasks.controls.append(task_view)
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
                self.tasks.controls.remove(task_view)
                self.update()
                break

    def task_edit(self, task_view, new_name):
        self.db.update_task(task_view.task.uuid, new_name, task_view.task.completed)
        task_view.task.name = new_name
        task_view.display_task.label = new_name
        self.update()

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
