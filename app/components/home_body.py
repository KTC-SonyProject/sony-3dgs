from flet import (
    Card,
    Column,
    ListTile,
    Text,
    TextButton,
    Icon,
    icons,
    MainAxisAlignment,
    Container,
    Row,
)





class HomeBody(Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.controls = [
            self.home_card(
                title="Voice",
                subtitle="AIと会話を通じて展示物の情報について質問したり、画面の操作を行うことができます。",
                icon=icons.VOICE_CHAT,
                go_page="voice",
            ),
            self.home_card(
                title="Documents",
                subtitle="展示物の情報を閲覧することができます。",
                icon=icons.DESCRIPTION,
                go_page="documents",
            ),
            self.home_card(
                title="Settings",
                subtitle="アプリケーションの設定を変更することができます。",
                icon=icons.SETTINGS,
                go_page="settings",
            ),
        ]

    def tap_go_page(self, e, go_page):
        e.page.route = f"/{go_page}"
        e.page.update()

    def home_card(self, title="title", subtitle="subtitle", icon=icons.ALBUM, go_page="page"):
        return Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            leading=Icon(icon),
                            title=Text(title, font_family="bold", weight="bold", size=20),
                            subtitle=Text(subtitle),
                        ),
                        Row(
                            [TextButton("Go Page", on_click=lambda e: self.tap_go_page(e, go_page))],
                            alignment=MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=500,
                padding=10,
            ),
        )
