import json

import flet as ft
from flet import (
    Page,
    ScrollMode,
    app,
)

from app.views import MyView


def load_settings():
    """設定をファイルから読み込む"""
    try:
        with open("local.settings.json") as f:
            return json.load(f)
    except FileNotFoundError:
        settings = {
            "use_postgres": False,
            "postgres_config": {
                "host": "postgres",
                "port": 5432,
                "database": "main_db",
                "user": "postgres",
                "password": "postgres",
            },
        }
        with open("local.settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        return settings
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}


def main(page: Page):
    page.title = "Spadge"
    page.scroll = ScrollMode.AUTO
    page.padding = 10

    page.data = {
        "settings_file": "local.settings.json",
        "settings": load_settings,
    }

    page.fonts = {
        "default": "/fonts/Noto_Sans_JP/static/NotoSansJP-Regular.ttf",
        "bold": "/fonts/Noto_Sans_JP/static/NotoSansJP-Black.ttf",
    }

    page.window.width = 1000
    page.window.height = 900
    page.window.min_width = 800
    page.window.min_height = 600


    theme = ft.Theme()
    theme.font_family = "default"
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
