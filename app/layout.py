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


class MyLayout(View):
    def __init__(self, page: Page, route='/'):
        super().__init__()
        self.page = page
        self.route = route
        if self.route=='/':
            self.page_title = 'Home'
        elif self.route=='/about':
            self.page_title = 'About'
        elif self.route=='/contact':
            self.page_title = 'Contact'
        elif self.route=='/chat':
            self.page_title = 'Chat'

        self.controls = [
            AppHeader(self.page, self.page_title.upper()),
            Row(
                alignment=MainAxisAlignment.START,
                vertical_alignment=CrossAxisAlignment.START,
                expand=True,
                # 基本はSidebarとContentBodyを表示し、/chatの場合はChatを表示
                controls=[
                    Sidebar(self.page),
                    ContentBody(self.page_title.upper() + ' Page')
                ] if self.route != '/chat' else [
                    ChatBody(self.page)
                ],
            ),
        ]
