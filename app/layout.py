from flet import CrossAxisAlignment, MainAxisAlignment, Page, ScrollMode, View

from app.components.body import ContentBody
from app.components.chat import ChatBody
from app.components.documents_body import DocumentsBody
from app.components.header import AppHeader
from app.components.home_body import HomeBody
from app.components.settings_body import SettingsBody
from app.components.top_body import TopBody
from app.components.voice_body import VoiceBody


class MyLayout(View):
    def __init__(self, page: Page, route='/'):
        super().__init__()
        self.page = page
        self.route = route
        self.scroll = ScrollMode.AUTO
        self.vertical_alignment = MainAxisAlignment.CENTER
        self.horizontal_alignment = CrossAxisAlignment.CENTER

        # スクロールモードを設定しているとエラーが発生するため、チャットページのみスクロールモードを無効にする
        if self.route == '/chat':
            self.scroll = None

        self.route_config = {
            '/': {
                'title': 'Top',
                'layout': TopBody(self.page),
            },
            '/home': {
                'title': 'Home',
                'layout': HomeBody(self.page),
            },
            '/voice': {
                'title': 'Voice',
                'layout': VoiceBody(self.page),
            },
            '/documents': {
                'title': 'Documents',
                'layout': DocumentsBody(self.page),
            },
            '/settings': {
                'title': 'Settings',
                'layout': SettingsBody(self.page),
            },
            '/chat': {
                'title': 'Chat',
                'layout': ChatBody(self.page),
            },
        }

        self.default_route_config = {
            'title': '404 Page Not Found',
            'layout': ContentBody(self.page, '404 Page Not Found'),
        }

        self.route_info = self.route_config.get(self.route, self.default_route_config)

        self.controls = [
            AppHeader(self.page, self.route_info['title'].upper()),
            self.route_info['layout'], # ルートごとに適切なレイアウトを取得
        ]
