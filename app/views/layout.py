import logging

from flet import (
    Page,
    ScrollMode,
    TemplateRoute,
    View,
)

from app.components.body import ContentBody
from app.components.chat import ChatBody
from app.components.documents_body import DocumentsBody, EditDocumentBody
from app.components.header import AppHeader
from app.components.home_body import HomeBody
from app.components.top_body import TopBody
from app.components.unity_body import UnityBody
from app.components.voice_body import VoiceBody
from app.views.settings_view import SettingsView

logger = logging.getLogger(__name__)

class MyLayout(View):
    def __init__(self, page: Page, route='/'):
        super().__init__()
        self.page = page
        self.route = route
        self.expand = True
        self.scroll = None

        # スクロールモードを設定しているとエラーが発生するため、チャットページのみスクロールモードを無効にする
        if self.route == '/':
            self.scroll = ScrollMode.AUTO

        self.troute = TemplateRoute(self.route)

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
                # 'layout': SettingsBody(self.page),
                'layout': SettingsView(self.page, self.page.data['settings']),
            },
            '/chat': {
                'title': 'Chat',
                'layout': ChatBody(self.page),
            },
            '/unity': {
                'title': 'Unity',
                'layout': UnityBody(self.page),
            },
        }

        self.default_route_config = {
            'title': '404 Page Not Found',
            'layout': ContentBody(self.page, '404 Page Not Found'),
        }

        if self.troute.match("/documents/:document_id"):
            self.route_info = {
                'title': 'Document',
                'layout': DocumentsBody(self.page, self.troute.document_id),
            }
            logger.debug(f"Document ID: {self.troute.document_id}")
        elif self.troute.match("/documents/:document_id/edit"):
            self.route_info = {
                "title": "Edit Document",
                "layout": EditDocumentBody(self.page, self.troute.document_id),
            }
            logger.debug(f"Edit Document ID: {self.troute.document_id}")
        else:
            self.route_info = self.route_config.get(self.route, self.default_route_config)
            logger.debug(f"Route: {self.route}")

        self.controls = [
            AppHeader(self.page, self.route_info['title'].upper()),
            self.route_info['layout'], # ルートごとに適切なレイアウトを取得
        ]
