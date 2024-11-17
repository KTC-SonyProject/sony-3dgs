import json
from flet import (
    Banner,
    Column,
    Text,
    ListTile,
    TextField,
    Switch,
    ElevatedButton,
    Divider,
    TextButton,
    Page,
    IconButton,
    icons,
)



class SettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 10
        self.settings_file = "local.settings.json"

        # 初期設定をロード
        self.settings = self.load_settings()


        # レイアウト
        self.controls = [
            Text("Settings", size=24, weight="bold"),
            Divider(),
            Text("Account Information", size=18),
            TextField(
                label="Username",
                value=self.settings.get("username", ""),
                on_change=lambda e: self.settings.update({"username": e.control.value}),
            ),
            TextField(
                label="Password",
                value=self.settings.get("password", ""),
                on_change=lambda e: self.settings.update({"password": e.control.value}),
            ),
            Divider(),
            ElevatedButton("Save Settings", on_click=self.save_settings),
        ]

    def load_settings(self):
        """設定をファイルから読み込む"""
        try:
            with open(self.settings_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "username": "",
                "password": "",
            }
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}

    def save_settings(self, e):
        """設定をファイルに保存する"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            self.show_banner(e, "success")
        except Exception:
            self.show_banner(e, "error")

    def banner_message(self, status):
        """バナーメッセージを表示する"""
        self.banner = Banner(
            bgcolor="red" if status == "error" else "green",
            content=Text("Settings saved successfully!" if status == "success" else "Error saving settings!"),
            actions=[IconButton(icon=icons.CLOSE, on_click=self.close_banner)],
        )
        return self.banner

    def close_banner(self, e):
        """バナーメッセージを閉じる"""
        self.banner.open = False
        e.control.page.update()

    def show_banner(self, e, status):
        """バナーメッセージを表示する"""
        e.control.page.overlay.append(self.banner_message(status))
        self.banner.open = True
        e.control.page.update()

