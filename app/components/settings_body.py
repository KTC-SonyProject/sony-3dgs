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

    def get_setting_value(self, key):
        """設定の値を取得する"""
        keys = key.split(".")
        target = self.settings
        for k in keys:
            if k not in target:
                raise ValueError(f"Key {k} not found in settings")
            target = target[k]
        return target

    def update_settings(self, key):
        """設定を更新する"""
        def handler(e):
            keys = key.split(".")
            target = self.settings
            for k in keys[:-1]:
                if k not in target:
                    raise ValueError(f"Key {k} not found in settings")
                target = target[k]
            target[keys[-1]] = e.control.value
        return handler


class GeneralSettingsColumn(BaseSettingsColumn):
    def __init__(self, page: Page, settings: dict):
        super().__init__(page, settings, "General Settings")

    def create_settings_controls(self):
        return Column(
                    spacing=20,
                    controls=[
                        TextField(
                            label="App Title",
                            value=self.get_setting_value("app_name"),
                            on_change=self.update_settings("app_name"),
                        ),
                        TextField(
                            label="App Description",
                            value=self.get_setting_value("app_description"),
                            on_change=self.update_settings("app_description"),
                        ),
                    ]
                )

class DBSettingsColumn(BaseSettingsColumn):
    def __init__(self, page: Page, settings: dict):
        super().__init__(page, settings, "Database Settings")

    def on_change_use_postgres(self, e):
        """PostgreSQLの使用を切り替える"""
        self.update_settings("use_postgres")(e)
        self.controls[2].controls[1].visible = e.control.value
        self.page.update()

    def create_settings_controls(self):
        return Column(
                    spacing=20,
                    controls=[
                        Switch(
                            label="Use PostgreSQL",
                            value=self.get_setting_value("use_postgres"),
                            on_change=self.on_change_use_postgres,
                        ),
                        Column(
                            spacing=10,
                            visible=self.get_setting_value("use_postgres"),
                            controls=[
                                Text("PostgreSQL Settings", size=20),
                                Divider(),
                                TextField(
                                    label="Host",
                                    value=self.get_setting_value("postgres_settings.host"),
                                    on_change=self.update_settings("postgres_settings.host"),
                                ),
                                TextField(
                                    label="Port",
                                    value=self.get_setting_value("postgres_settings.port"),
                                    on_change=self.update_settings("postgres_settings.port"),
                                    input_filter=NumbersOnlyInputFilter(),
                                ),
                                TextField(
                                    label="Database",
                                    value=self.get_setting_value("postgres_settings.database"),
                                    on_change=self.update_settings("postgres_settings.database"),
                                ),
                                TextField(
                                    label="User",
                                    value=self.get_setting_value("postgres_settings.user"),
                                    on_change=self.update_settings("postgres_settings.user"),
                                ),
                                TextField(
                                    label="Password",
                                    value=self.get_setting_value("postgres_settings.password"),
                                    password=True,
                                    can_reveal_password=True,
                                    on_change=self.update_settings("postgres_settings.password"),
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
                        value=self.get_setting_value("azure_llm_settings.endpoint"),
                        on_change=self.update_settings("azure_llm_settings.endpoint"),
                    ),
                    TextField(
                        label="API Key",
                        value=self.get_setting_value("azure_llm_settings.api_key"),
                        password=True,
                        can_reveal_password=True,
                        on_change=self.update_settings("azure_llm_settings.api_key"),
                    ),
                    TextField(
                        label="Deployment Name",
                        value=self.get_setting_value("azure_llm_settings.deployment_name"),
                        on_change=self.update_settings("azure_llm_settings.deployment_name"),
                    ),
                    TextField(
                        label="Deployment Name (Embeddings)",
                        value=self.get_setting_value("azure_llm_settings.deployment_embdding_name"),
                        on_change=self.update_settings("azure_llm_settings.deployment_embdding_name"),
                    ),
                    TextField(
                        label="API Version",
                        value=self.get_setting_value("azure_llm_settings.api_version"),
                        on_change=self.update_settings("azure_llm_settings.api_version"),
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
        self.update_settings("llm_provider")(e)
        self.controls[2].controls[1] = self.get_llm_provider_control(e.control.value)
        self.page.update()

    def on_change_use_langsmith(self, e):
        """LangSmithの使用を切り替える"""
        self.update_settings("use_langsmith")(e)
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
                            value=self.get_setting_value("llm_provider"),
                            options=[
                                dropdown.Option("azure"),
                                dropdown.Option("gemini"),
                                dropdown.Option("ollama"),
                            ],
                            on_change=self.on_change_llm_provider,
                        ),
                        self.get_llm_provider_control(self.get_setting_value("llm_provider")),
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
                                    value=self.get_setting_value("use_langsmith"),
                                    on_change=self.on_change_use_langsmith,
                                ),
                                Column(
                                    visible=self.get_setting_value("use_langsmith"),
                                    controls=[
                                        TextField(
                                            label="project name",
                                            value=self.get_setting_value("langsmith_settings.project_name"),
                                            on_change=self.update_settings("langsmith_settings.project_name"),
                                        ),
                                        TextField(
                                            label="LangSmith API Key",
                                            value=self.get_setting_value("langsmith_settings.api_key"),
                                            password=True,
                                            can_reveal_password=True,
                                            on_change=self.update_settings("langsmith_settings.api_key"),
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

