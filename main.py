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
from core.theme_manager import ThemeManager

def main(page: ft.Page):
    page.title = "Smart Todo App. Copyright © 2024-2025, Alexander Suvorov; All rights reserved."
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE


    theme_manager = ThemeManager()
    page.theme_mode = (
        ft.ThemeMode.DARK if theme_manager.theme == "dark" else ft.ThemeMode.LIGHT
    )


    def toggle_theme(e):
        theme_manager.toggle()
        page.theme_mode = (
            ft.ThemeMode.DARK if theme_manager.theme == "dark" else ft.ThemeMode.LIGHT
        )
        page.update()


    page.appbar = ft.AppBar(
        title=ft.Text("Smart Todo App"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.BRIGHTNESS_6_OUTLINED,
                tooltip="Toggle Dark/Light Mode",
                on_click=toggle_theme,
            ),
        ],
    )


    todo_app = TodoApp()
    page.add(todo_app)
    todo_app.load_tasks()


ft.app(main)
