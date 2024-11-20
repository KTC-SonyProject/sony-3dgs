from flet import (
    AppBar,
    Container,
    Icon,
    IconButton,
    MainAxisAlignment,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Text,
    colors,
    icons,
    margin,
)


class AppHeader(AppBar):
    def __init__(self, page: Page, page_title: str="Example"):
        super().__init__()
        self.page = page
        self.page_title = page_title
        self.toggle_dark_light_icon = IconButton(
            icon=icons.LIGHT_MODE_OUTLINED,
            selected_icon =icons.DARK_MODE_OUTLINED,
            tooltip="switch light and dark mode",
            on_click=self.toggle_icon,
        )
        self.chat_icon = IconButton(
            icon=icons.CHAT_BUBBLE_OUTLINE,
            tooltip="Chat",
            on_click=lambda _: self.page.go("/chat"),
        )
        self.appbar_items = [
            PopupMenuItem(text="Top", on_click=lambda _: self.page.go("/")),
            PopupMenuItem(text="Home", on_click=lambda _: self.page.go("/home")),
            PopupMenuItem(),
            PopupMenuItem(text="Voice", on_click=lambda e: self.page.go("/voice")),
            PopupMenuItem(text="Documents", on_click=lambda e: self.page.go("/documents")),
            PopupMenuItem(),
            PopupMenuItem(text="Settings", on_click=lambda e: self.page.go("/settings")),
        ]
        self.leading=Icon(icons.TRIP_ORIGIN_ROUNDED)
        self.leading_width=60
        self.title=Text(value=self.page_title, size=32, text_align="center")
        self.center_title=False
        self.toolbar_height=75
        self.bgcolor=colors.SURFACE_VARIANT
        self.actions=[
            Container(
                margin=margin.only(left=50, right=25),
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.chat_icon,
                        self.toggle_dark_light_icon,
                        PopupMenuButton(
                            items=self.appbar_items
                        ),
                    ],
                ),
            )
        ]

    def toggle_icon(self, e):
        self.page.theme_mode = "light" if self.page.theme_mode == "dark" else "dark"
        self.toggle_dark_light_icon.selected = not self.toggle_dark_light_icon.selected
        self.page.update()




if __name__ == '__main__':
    import flet as ft
    def main(page: ft.Page) -> None:
        page.title = 'AI Chat'
        example = AppHeader(page)
        page.add(example)

    ft.app(main)
