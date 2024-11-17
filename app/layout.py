from flet import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Row,
    View,
)

from app.components.body import ContentBody
from app.components.chat import ChatBody
from app.components.header import AppHeader
from app.components.sidebar import Sidebar
from app.components.top_body import TopBody
from app.components.home_body import HomeBody
from app.components.voice_body import VoiceBody
from app.components.documents_body import DocumentsBody
from app.components.settings_body import SettingsBody


class MyLayout(View):
    def __init__(self, page: Page, route='/'):
        super().__init__()
        self.page = page
        self.route = route

        self.routes = {
            '/': 'Top',
            '/home': 'Home',
            '/voice': 'Voice',
            '/documents': 'Documents',
            '/settings': 'Settings',
            '/chat': 'Chat',
        }

        self.page_title = self.routes.get(route, '404 Page Not Found')

        self.controls = [
            AppHeader(self.page, self.page_title.upper()),
            self.get_body_layout(), # ルートごとに適切なレイアウトを取得
        ]

    def get_body_layout(self):
        """ルートごとに適切なレイアウトを取得"""
        if self.route == '/':
            return Row(
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                controls=[
                    TopBody()
                ],
            )
        elif self.route == '/home':
            return Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    HomeBody()
                ],
            )
        elif self.route == '/voice':
            return Row(
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                controls=[
                    VoiceBody()
                ],
            )
        elif self.route == '/documents':
            return Row(
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                controls=[
                    DocumentsBody()
                ],
            )
        elif self.route == '/settings':
            return Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                controls=[
                    SettingsBody(self.page)
                ],
            )
        elif self.route == '/chat':
            return Row(
                expand=True,
                controls=[
                    ChatBody(self.page)
                ],
            )
        else:
            return Row(
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                controls=[
                    Sidebar(self.page),
                    ContentBody(self.page_title.upper() + ' Page')
                ],
            )
