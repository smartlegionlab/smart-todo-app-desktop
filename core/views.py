# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024-2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import flet as ft
from datetime import datetime


class TaskView(ft.Column):
    def __init__(self, task, on_status_change, on_delete, on_edit, on_move_up, on_move_down):
        super().__init__()
        self.task = task
        self.on_status_change = on_status_change
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down

        self.task_checkbox = ft.Checkbox(value=self.task.completed, on_change=self.status_changed)
        self.task_text = ft.Text(value=self.task.name, no_wrap=False)

        self.edit_name = ft.TextField(expand=1, value=self.task.name)

        if isinstance(self.task.created_date, str):
            created_date = datetime.fromisoformat(self.task.created_date)
        else:
            created_date = self.task.created_date

        self.created_date_text = ft.Text(
            value=f"Created: {created_date.strftime('%Y-%m-%d %H:%M')}",
            size=12,
            color=ft.colors.GREY_500
        )

        self.display_view = self.create_display_view()
        self.edit_view = self.create_edit_view()

        self.controls = [self.display_view, self.edit_view]

    def create_display_view(self):
        return ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Row(
                            controls=[
                                self.task_checkbox,
                                self.task_text,
                            ],
                            expand=True,
                            wrap=True,
                        ),
                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_UPWARD,
                                    tooltip="Move up",
                                    on_click=self.move_up_clicked,
                                    icon_size=16
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_DOWNWARD,
                                    tooltip="Move down",
                                    on_click=self.move_down_clicked,
                                    icon_size=16
                                ),
                                ft.IconButton(
                                    icon=ft.icons.CREATE_OUTLINED,
                                    tooltip="Edit",
                                    on_click=self.edit_clicked
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_OUTLINE,
                                    tooltip="Delete",
                                    on_click=self.delete_clicked
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Container(
                    content=self.created_date_text,
                    padding=ft.padding.only(left=40)
                )
            ]
        )

    def create_edit_view(self):
        return ft.Column(
            visible=False,
            controls=[
                ft.Row(
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
                ),
                ft.Container(
                    content=self.created_date_text,
                    padding=ft.padding.only(left=40)
                )
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
        self.task.completed = self.task_checkbox.value
        self.on_status_change(self.task)

    def delete_clicked(self, e):
        self.on_delete(self.task)

    def move_up_clicked(self, e):
        self.on_move_up(self.task)

    def move_down_clicked(self, e):
        self.on_move_down(self.task)
