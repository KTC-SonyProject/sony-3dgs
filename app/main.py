import flet as ft
from flet import (
    Page,
    app,
)

from app.views import MyView


def main(page: Page):
    page.title = "Sony × 3DGS App"
    page.padding = 10

    page.window.width = 1000
    page.window.height = 900
    page.window.min_width = 800
    page.window.min_height = 600


    theme = ft.Theme()
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    theme.page_transitions.macos = ft.PageTransitionTheme.NONE
    theme.page_transitions.linux = ft.PageTransitionTheme.NONE
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.update()

    MyView(page)

if __name__ == '__main__':
    app(target=main)
