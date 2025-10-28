# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024-2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import flet as ft
from core.controllers import TodoApp


def main(page: ft.Page):
    page.title = "Smart Todo App. Copyright © 2024-2025, Alexander Suvorov; All rights reserved."
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    todo_app = TodoApp()
    page.add(todo_app)
    todo_app.load_tasks()


ft.app(main)
