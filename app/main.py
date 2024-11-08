from flet import (
    Page,
    app,
)

from app.layout import MyLayout


def main(page: Page):
    page.title = "Sony × 3DGS App"
    page.padding = 10

    page.window.width = 1000
    page.window.height = 900
    page.window.min_width = 800
    page.window.min_height = 600

    page.add(MyLayout(page))

if __name__ == '__main__':
    app(target=main)
