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

    def get_priority_color(self, priority):
        if priority == "High":
            return ft.colors.RED_700
        elif priority == "Medium":
            return ft.colors.ORANGE_600
        elif priority == "Low":
            return ft.colors.YELLOW_600
        return ft.colors.WHITE

    def filter_by_priority(self, e):
        self.selected_priority = e.control.value
        self.update()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.new_task = ft.TextField(hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True)
        self.priority_dropdown = ft.Dropdown(options=[ft.dropdown.Option("Low"),ft.dropdown.Option("Medium"),ft.dropdown.Option("High"),],value="Medium",width=120)
        self.tasks = ft.Column()
        self.items_left = ft.Text("0 items left")
        self.progress_bar = ft.ProgressBar(value=0, width=300, color=ft.colors.GREEN_400)
        self.filter = self.create_filter()

        self.sort_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Default"),
                ft.dropdown.Option("Priority"),
                ft.dropdown.Option("Date"),
            ],
            value="Default",
            on_change=self.sort_tasks,
            width=150,
        )

        self.controls = [
            ft.Row(
                [ft.Text(value="Todo List", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    self.priority_dropdown,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                ],
                spacing=10,
            ),
            ft.Row(
                controls=[
                    ft.Dropdown(
                        options=[ft.dropdown.Option("All"), ft.dropdown.Option("Low"), ft.dropdown.Option("Medium"),
                                 ft.dropdown.Option("High")],
                        value="All",
                        width=120,
                        on_change=self.filter_by_priority,
                    ),
                    self.sort_dropdown,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    self.items_left,
                                    ft.OutlinedButton(text="Clear completed", on_click=self.clear_clicked),
                                ],
                            ),
                            self.progress_bar,
                        ],
                    ),
                ],
            ),
        ]

        self.selected_priority = "All"

    def create_filter(self):
        return ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="active"), ft.Tab(text="all"), ft.Tab(text="completed")],
        )

    def load_tasks(self):
        self.tasks.controls.clear()
        tasks_data = self.db.get_all_tasks()

        icon_map = {
            "High": ft.icons.PRIORITY_HIGH,
            "Medium": ft.icons.FLAG,
            "Low": ft.icons.LABEL,
        }

        for row in tasks_data:
            if len(row) == 6:
                task_uuid, task_name, completed, created_date, sort_order, priority = row
            else:
                task_uuid, task_name, completed, created_date, sort_order = row
                priority = "Medium"

            completed = bool(completed)
            task = Task(task_uuid, task_name, completed, created_date, sort_order, priority)

            task_view = TaskView(
                task,
                self.task_status_change,
                self.task_delete,
                self.task_edit,
                self.task_move_up,
                self.task_move_down
            )

            task_view.task_text.color = self.get_priority_color(task.priority)
            task_view.task_text.weight = ft.FontWeight.BOLD
            task_view.task_text.size = 20


            priority_icon = ft.Icon(
                name=icon_map.get(task.priority, ft.icons.LABEL),
                color=self.get_priority_color(task.priority),
                size=20,
            )


            if hasattr(task_view, "controls") and isinstance(task_view.controls, list):
                task_view.controls.insert(0, priority_icon)


            task_view.animate_opacity = 300
            task_view.opacity = 0
            self.tasks.controls.append(task_view)
            self.update()
            task_view.opacity = 1
            self.update()

        self.update()

    def add_clicked(self, e):
        if self.new_task.value:
            task_name = self.new_task.value
            priority = self.priority_dropdown.value
            task = Task(task_name=task_name, priority=priority)
            self.db.add_task(task.uuid, task_name, priority)
            self.load_tasks()
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.db.update_task(task.uuid, task.name, task.completed)
        self.update()

    def task_delete(self, task):
        for task_view in self.tasks.controls[:]:
            if task_view.task.uuid == task.uuid:
                self.db.delete_task(task.uuid)
                self.db.reorder_tasks()
                self.tasks.controls.remove(task_view)
                self.load_tasks()
                break
        self.update()

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
        completed_tasks = [task_view for task_view in self.tasks.controls[:] if task_view.task.completed]
        for task_view in completed_tasks:
            self.task_delete(task_view.task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task_view in self.tasks.controls:
            visible = True
            if status == "active":
                visible = not task_view.task.completed
            elif status == "completed":
                visible = task_view.task.completed

            if self.selected_priority != "All":
                visible = visible and (task_view.task.priority == self.selected_priority)

            task_view.visible = visible

            if not task_view.task.completed:
                count += 1

        self.items_left.value = f"{count} active task(s) left"
        total = len(self.tasks.controls)
        completed = total - count
        self.progress_bar.value = completed / total if total > 0 else 0
        progress = completed / total if total > 0 else 0
        self.progress_bar.value = progress

        if progress == 1:
            self.progress_bar.color = ft.colors.GREEN_600
        elif progress >= 0.5:
            self.progress_bar.color = ft.colors.AMBER_400
        else:
            self.progress_bar.color = ft.colors.RED_400

    def sort_tasks(self, e):
        sort_type = self.sort_dropdown.value
        if sort_type == "Priority":
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            self.tasks.controls.sort(
                key=lambda t: priority_order.get(t.task.priority, 0), reverse=True
            )
        elif sort_type == "Date":
            self.tasks.controls.sort(
                key=lambda t: t.task.created_date, reverse=True
            )
        else:
            self.tasks.controls.sort(key=lambda t: t.task.sort_order)

        self.update()
