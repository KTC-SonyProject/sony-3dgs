from dataclasses import dataclass

from flet import (
    Card,
    Column,
    Container,
    Icon,
    Icons,
    ListTile,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextButton,
    alignment,
    app,
)


@dataclass
class HomeCardItem:
    title: str
    subtitle: str
    icon: str
    go_page: str


class HomeCard(Card):
    def __init__(self, page: Page, card_item: HomeCardItem):
        super().__init__()
        self.page = page
        self.content = Container(
            content=Column(
                [
                    ListTile(
                        leading=Icon(card_item.icon),
                        title=Text(card_item.title, font_family="bold", weight="bold", size=20),
                        subtitle=Text(card_item.subtitle),
                    ),
                    Row(
                        [TextButton("Go Page", on_click=lambda _: self.page.go(f"/{card_item.go_page}"))],
                        alignment=MainAxisAlignment.END,
                    ),
                ]
            ),
            width=500,
            padding=10,
        )



class HomeList(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.alignment = MainAxisAlignment.CENTER

        self.card_items = [
            HomeCardItem(
                title="Voice",
                subtitle="AIと会話を通じて展示物の情報について質問したり、画面の操作を行うことができます。",
                icon=Icons.VOICE_CHAT,
                go_page="voice",
            ),
            HomeCardItem(
                title="Documents",
                subtitle="展示物の情報を閲覧することができます。",
                icon=Icons.DESCRIPTION,
                go_page="documents",
            ),
            HomeCardItem(
                title="Settings",
                subtitle="アプリケーションの設定を変更することができます。",
                icon=Icons.SETTINGS,
                go_page="settings",
            ),
        ]

        self.controls = self.create_home_card(self.card_items)

    def create_home_card(self, card_items: list[HomeCardItem]):
        items = []

        for card_item in card_items:
            items.append(HomeCard(self.page, card_item))

        return items


class HomeBody(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment = alignment.center
        self.height = self.page.height
        self.page.on_resized = self.on_resized
        self.content = HomeList(self.page)

    def on_resized(self, e):
        self.height = self.page.height
        self.page.update()


if __name__ == "__main__":

    def main(page: Page) -> None:
        page.title = "test app"
        page.scroll = "auto"
        chat_page = HomeBody(page)
        page.add(chat_page)

    app(main)
