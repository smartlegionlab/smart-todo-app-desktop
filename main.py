# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import flet as ft
from controllers.controllers import TodoApp


def main(page: ft.Page):
    page.title = "Smart ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    todo_app = TodoApp()
    page.add(todo_app)
    todo_app.load_tasks()


ft.app(main)
