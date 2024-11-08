from flet import (
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Row,
)

from app.components.body import ContentBody
from app.components.header import AppHeader
from app.components.sidebar import Sidebar


class MyLayout(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START

        AppHeader(page, 'HOME') # インスタンス生成時にpage.appbarにナビゲーションバーが設定される
        self.controls = [ Sidebar(), ContentBody() ]
