from core.db import Database


class ThemeManager:
    def __init__(self):
        self.db = Database()
        self.theme = self.load()

    def load(self):
        return self.db.get_setting('theme', 'dark')

    def save(self):
        self.db.set_setting('theme', self.theme)

    def toggle(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.save()
