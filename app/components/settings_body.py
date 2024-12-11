import json
import time

from flet import (
    Banner,
    Column,
    Container,
    CrossAxisAlignment,
    Divider,
    Dropdown,
    ElevatedButton,
    IconButton,
    NumbersOnlyInputFilter,
    Page,
    Row,
    ScrollMode,
    Switch,
    Tab,
    TabAlignment,
    Tabs,
    Text,
    TextField,
    alignment,
    dropdown,
    icons,
)

from app.ai.settings import langsmith_settigns
from app.db_conn import DatabaseHandler
from app.settings import load_settings


class BaseSettingsColumn(Column):
    def __init__(self, page: Page, settings: dict, title: str):
        super().__init__()
        self.page = page
        self.settings = settings
        self.expand = True
        self.controls = [
            Container(
                padding=10,
                alignment=alignment.center,
                content=Text(title, size=30),
            ),
            Divider(),
            self.create_settings_controls()
        ]

    def create_settings_controls(self):
        """各設定のコントロールを生成する（サブクラスで実装）"""
        return Column()


class GeneralSettingsColumn(BaseSettingsColumn):
    def __init__(self, page: Page, settings: dict):
        super().__init__(page, settings, "General Settings")

    def create_settings_controls(self):
        return Column(
                    spacing=20,
                    controls=[
                        TextField(
                            label="App Title",
                            value=self.settings.get("app_name", ""),
                            on_change=lambda e: self.settings.update({"app_name": e.control.value}),
                        ),
                        TextField(
                            label="App Description",
                            value=self.settings.get("app_description", ""),
                            on_change=lambda e: self.settings.update({"app_description": e.control.value}),
                        ),
                    ]
                )

class DBSettingsColumn(BaseSettingsColumn):
    def __init__(self, page: Page, settings: dict):
        super().__init__(page, settings, "Database Settings")

    def on_change_use_postgres(self, e):
        """PostgreSQLの使用を切り替える"""
        self.settings["use_postgres"] = e.control.value
        self.controls[2].controls[1].visible = e.control.value
        self.page.update()

    def create_settings_controls(self):
        return Column(
                    spacing=20,
                    controls=[
                        Switch(
                            label="Use PostgreSQL",
                            value=self.settings.get("use_postgres", False),
                            on_change=self.on_change_use_postgres,
                        ),
                        Column(
                            spacing=10,
                            visible=self.settings.get("use_postgres", False),
                            controls=[
                                Text("PostgreSQL Settings", size=20),
                                Divider(),
                                TextField(
                                    label="Host",
                                    value=self.settings["postgres_settings"].get("host", ""),
                                    on_change=lambda e: self.settings["postgres_settings"].update(
                                        {"host": e.control.value}
                                    ),
                                ),
                                TextField(
                                    label="Port",
                                    value=self.settings["postgres_settings"].get("port", ""),
                                    on_change=lambda e: self.settings["postgres_settings"].update(
                                        {"port": int(e.control.value)}
                                    ),
                                    input_filter=NumbersOnlyInputFilter(),
                                ),
                                TextField(
                                    label="Database",
                                    value=self.settings["postgres_settings"].get("database", ""),
                                    on_change=lambda e: self.settings["postgres_settings"].update(
                                        {"database": e.control.value}
                                    ),
                                ),
                                TextField(
                                    label="User",
                                    value=self.settings["postgres_settings"].get("user", ""),
                                    on_change=lambda e: self.settings["postgres_settings"].update(
                                        {"user": e.control.value}
                                    ),
                                ),
                                TextField(
                                    label="Password",
                                    value=self.settings["postgres_settings"].get("password", ""),
                                    password=True,
                                    can_reveal_password=True,
                                    on_change=lambda e: self.settings["postgres_settings"].update(
                                        {"password": e.control.value}
                                    ),
                                ),
                            ],
                        ),
                    ],
                )

class LLMSettingsColumn(BaseSettingsColumn):
    def __init__(self, page: Page, settings: dict):
        super().__init__(page, settings, "LLM Settings")

    def get_llm_provider_control(self, llm_provider):
        """LLMプロバイダーのコントロールを生成する"""
        if llm_provider == "azure":
            return Column(
                spacing=10,
                data="azure",
                controls=[
                    Text("Azure LLM Settings", size=20),
                    Divider(),
                    TextField(
                        label="Endpoint",
                        value=self.settings.get("azure_llm_settings", {}).get("endpoint", ""),
                        on_change=lambda e: self.settings["azure_llm_settings"].update({"endpoint": e.control.value}),
                    ),
                    TextField(
                        label="API Key",
                        value=self.settings.get("azure_llm_settings", {}).get("api_key", ""),
                        password=True,
                        can_reveal_password=True,
                        on_change=lambda e: self.settings["azure_llm_settings"].update({"api_key": e.control.value}),
                    ),
                    TextField(
                        label="Deployment Name",
                        value=self.settings.get("azure_llm_settings", {}).get("deployment_name", ""),
                        on_change=lambda e: self.settings["azure_llm_settings"].update(
                            {"deployment_name": e.control.value}
                        ),
                    ),
                    TextField(
                        label="Deployment Name (Embeddings)",
                        value=self.settings.get("azure_llm_settings", {}).get("deployment_embdding_name", ""),
                        on_change=lambda e: self.settings["azure_llm_settings"].update(
                            {"deployment_embdding_name": e.control.value}
                        ),
                    ),
                    TextField(
                        label="API Version",
                        value=self.settings.get("azure_llm_settings", {}).get("api_version", ""),
                        on_change=(
                            lambda e: self.settings["azure_llm_settings"].update({"api_version": e.control.value})
                        ),
                    ),
                ],
            )
        elif llm_provider == "gemini":
            return Column(
                spacing=10,
                data="gemini",
                controls=[
                    Container(
                        padding=30,
                        alignment=alignment.center,
                        content=Text("Geminiはまだ実装されていません。", size=20, color="yellow"),
                    )
                ],
            )
        elif llm_provider == "ollama":
            return Column(
                spacing=10,
                data="ollama",
                controls=[
                    Container(
                        padding=30,
                        alignment=alignment.center,
                        content=Text("Ollamaはまだ実装されていません。", size=20, color="yellow"),
                    )
                ],
            )


    def on_change_llm_provider(self, e):
        """LLMプロバイダーを切り替える"""
        self.settings["llm_provider"] = e.control.value
        self.controls[2].controls[1] = self.get_llm_provider_control(e.control.value)
        self.page.update()

    def on_change_use_langsmith(self, e):
        """LangSmithの使用を切り替える"""
        self.settings["use_langsmith"] = e.control.value
        self.controls[2].controls[4].controls[4].visible = e.control.value
        self.page.update()

    def create_settings_controls(self):
        return Column(
                    expand=True,
                    scroll=ScrollMode.HIDDEN,
                    spacing=50,
                    controls=[
                        Dropdown(
                            label="LLM Provider",
                            value=self.settings.get("llm_provider", "azure"),
                            options=[
                                dropdown.Option("azure"),
                                dropdown.Option("gemini"),
                                dropdown.Option("ollama"),
                            ],
                            on_change=self.on_change_llm_provider,
                        ),
                        self.get_llm_provider_control(self.settings.get("llm_provider", "azure")),
                        Column(
                            spacing=10,
                            controls=[
                                Text(
                                    "Options",
                                    size=20,
                                ),
                                Divider(),
                                Text(
                                    "Chat履歴を効率的に管理するためにLangSmithを導入できます。",
                                    size=15,
                                ),
                                Switch(
                                    label="Use LangSmith",
                                    value=self.settings.get("use_langsmith", False),
                                    on_change=self.on_change_use_langsmith,
                                ),
                                Column(
                                    visible=self.settings.get("use_langsmith", False),
                                    controls=[
                                        TextField(
                                            label="project name",
                                            value=self.settings.get("langsmith_settings", {}).get("project_name", ""),
                                            on_change=lambda e: self.settings["langsmith_settings"].update(
                                                "project_name", e.control.value
                                            ),
                                        ),
                                        TextField(
                                            label="LangSmith API Key",
                                            value=self.settings.get("langsmith_settings", {}).get("api_key", ""),
                                            password=True,
                                            can_reveal_password=True,
                                            on_change=lambda e: self.settings["langsmith_settings"].update(
                                                "api_key", e.control.value
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )


class TabBody(Tab):
    def __init__(self, page: Page, title: str, settings: dict):
        super().__init__()
        self.page = page
        self.settings = settings
        self.text = title
        self.expand=True

        if title == "General":
            self.content = GeneralSettingsColumn(self.page, self.settings)
        elif title == "Database":
            self.content = DBSettingsColumn(self.page, self.settings)
        elif title == "LLM":
            self.content = LLMSettingsColumn(self.page, self.settings)
        else:
            self.content = Text("No settings available for this tab")


class SettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 10
        self.expand=True
        # self.alignment = MainAxisAlignment.START
        self.horizontal_alignment = CrossAxisAlignment.START

        # 初期設定をロード
        self.settings_file = self.page.data["settings_file"]
        self.settings = self.page.data["settings"]()

        self.controls = [
            Container(
                padding=10,
                alignment=alignment.center,
                content=Row(
                    spacing=20,
                    controls=[
                        Text("Settings", size=30),
                        ElevatedButton("Save Settings", on_click=self.save_settings),
                    ]
                ),
            ),
            Tabs(
                expand=True,
                selected_index=0,
                animation_duration=300,
                tab_alignment=TabAlignment.CENTER,
                tabs=[
                    TabBody(self.page, "General", self.settings["general_settings"]),
                    TabBody(self.page, "Database", self.settings["db_settings"]),
                    TabBody(self.page, "LLM", self.settings["llm_settings"]),
                ]
            ),
        ]


    def save_settings(self, e):
        """設定をファイルに保存する"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            self.page.data["db"] = DatabaseHandler(load_settings())
            langsmith_settigns()
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
        time.sleep(3)
        self.close_banner(e)

