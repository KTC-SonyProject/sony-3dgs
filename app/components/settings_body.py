import json

from flet import (
    Banner,
    Column,
    Divider,
    ElevatedButton,
    IconButton,
    NumbersOnlyInputFilter,
    Page,
    Switch,
    Text,
    TextField,
    icons,
)


class SettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 10

        # 初期設定をロード
        self.settings_file = self.page.data["settings_file"]
        self.settings = self.page.data["settings"]()



        # レイアウト
        self.controls = [
            Text("Settings", size=24, weight="bold"),
            Divider(),
            Text("Database Settings", size=18),
            Switch(
                label="Use PostgreSQL",
                value=self.settings.get("use_postgres", False),
                on_change=lambda e: self.on_change_use_postgres(e),
            ),
            Column(
                visible=self.settings.get("use_postgres", False),
                controls=[
                    TextField(
                        label="Host",
                        value=self.settings["postgres_config"].get("host", ""),
                        on_change=lambda e: self.settings["postgres_config"].update({"host": e.control.value}),
                    ),
                    TextField(
                        label="Port",
                        value=self.settings["postgres_config"].get("port", ""),
                        on_change=lambda e: self.settings["postgres_config"].update({"port": int(e.control.value)}),
                        input_filter=NumbersOnlyInputFilter(),
                    ),
                    TextField(
                        label="Database",
                        value=self.settings["postgres_config"].get("database", ""),
                        on_change=lambda e: self.settings["postgres_config"].update({"database": e.control.value}),
                    ),
                    TextField(
                        label="User",
                        value=self.settings["postgres_config"].get("user", ""),
                        on_change=lambda e: self.settings["postgres_config"].update({"user": e.control.value}),
                    ),
                    TextField(
                        label="Password",
                        value=self.settings["postgres_config"].get("password", ""),
                        on_change=lambda e: self.settings["postgres_config"].update({"password": e.control.value}),
                    ),
                ],
            ),
            Divider(),
            ElevatedButton("Save Settings", on_click=self.save_settings),
        ]


    def on_change_use_postgres(self, e):
        """PostgreSQLの使用を切り替える"""
        self.settings["use_postgres"] = e.control.value
        self.controls[4].visible = e.control.value
        self.page.update()

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

