from flet import (
    Container,
    CrossAxisAlignment,
    FloatingActionButton,
    Icon,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Page,
    Row,
    Text,
    alignment,
    border_radius,
    colors,
    icons,
)


class Sidebar(Container):
    def __init__(self, page:Page):
        super().__init__()
        self.page = page
        self.nav_rail_visible = True
        self.nav_rail_items = [
            NavigationRailDestination(
                icon=icons.FAVORITE_BORDER,
                selected_icon=icons.FAVORITE,
                label="Favorite"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.BOOKMARK_BORDER),
                selected_icon_content=Icon(icons.BOOKMARK),
                label="Bookmark"
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ]
        self.nav_rail = NavigationRail(
            height= 300,
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=FloatingActionButton(icon=icons.CREATE, text="ADD"),
            group_alignment=-0.9,
            destinations=self.nav_rail_items,
            on_change=self.tap_nav_icon,
        )
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
            tooltip="Collapse Nav Bar",
        )
        self.visible = self.nav_rail_visible
        self.content = Row(
            controls=[
                self.nav_rail,
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=480,
                    alignment=alignment.center_right,
                    width=2
                ),
                self.toggle_nav_rail_button,
            ],
            vertical_alignment=CrossAxisAlignment.START,
        )

    def toggle_nav_rail(self, e):
        self.nav_rail.visible = not self.nav_rail.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.toggle_nav_rail_button.tooltip = (
            "Open Side Bar" if self.toggle_nav_rail_button.selected else "Collapse Side Bar"
        )
        self.update()

    def tap_nav_icon(self, e):
        if e.control.selected_index == 0:
            self.page.go('/about')
        elif e.control.selected_index == 1:
            self.page.go('/contact')
        else:
            self.page.go('/')


if __name__ == '__main__':
    import flet as ft
    def main(page: ft.Page) -> None:
        page.title = 'Navigation Rail'
        sidebar = Sidebar(page)
        page.add(sidebar)

    ft.app(target=main)
