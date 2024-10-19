# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import flet as ft


class TaskView(ft.Column):
    def __init__(self, task, on_status_change, on_delete, on_edit):
        super().__init__()
        self.task = task
        print(self.task.__dict__)
        self.on_status_change = on_status_change
        self.on_delete = on_delete
        self.on_edit = on_edit

        self.display_task = ft.Checkbox(
            value=self.task.completed, label=self.task.name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1, value=self.task.name)

        self.display_view = self.create_display_view()
        self.edit_view = self.create_edit_view()

        self.controls = [self.display_view, self.edit_view]

    def create_display_view(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(icon=ft.icons.CREATE_OUTLINED, tooltip="Edit", on_click=self.edit_clicked),
                        ft.IconButton(icon=ft.icons.DELETE_OUTLINE, tooltip="Delete", on_click=self.delete_clicked),
                    ],
                ),
            ],
        )

    def create_edit_view(self):
        return ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update",
                    on_click=self.save_clicked
                ),
            ],
        )

    def edit_clicked(self, e):
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.on_edit(self, self.edit_name.value)
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.task.completed = self.display_task.value
        self.on_status_change(self.task)

    def delete_clicked(self, e):
        self.on_delete(self.task)
