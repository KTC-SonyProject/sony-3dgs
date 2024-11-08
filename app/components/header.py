from flet import (
    AppBar,
    Container,
    ElevatedButton,
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
            icon="light_mode",
            selected_icon = "dark_mode",
            tooltip="switch light and dark mode",
            on_click=self.toggle_icon,
        )
        self.appbar_items = [
            PopupMenuItem(text="Login"),
            PopupMenuItem(),
            PopupMenuItem(text="SignUp"),
            PopupMenuItem(),
            PopupMenuItem(text="Settings"),
        ]
        # Appのpage.appbarフィールドの設定
        self.page.appbar = AppBar(
            leading=Icon(icons.TRIP_ORIGIN_ROUNDED),
            leading_width=100,
            title=Text(value=self.page_title, size=32, text_align="center"),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                Container(
                    content=Row(
                        [
                            self.toggle_dark_light_icon,
                            ElevatedButton(text="SOMETHING"),
                            PopupMenuButton(
                                items=self.appbar_items
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )

    def toggle_icon(self, e):
        self.page.theme_mode = "light" if self.page.theme_mode == "dark" else "dark"
        self.toggle_dark_light_icon.selected = not self.toggle_dark_light_icon.selected
        self.page.update()
