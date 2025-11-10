import json
import os

SETTINGS_FILE = "data/settings.json"


class ThemeManager:
    def __init__(self):
        self.theme = "dark"
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.theme = data.get("theme", "dark")
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"theme": self.theme}, f)

    def toggle(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.save()