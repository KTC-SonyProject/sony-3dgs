"""
View用の共通基底クラスや抽象クラスを定義
"""

import logging

from flet import (
    Column,
    Container,
    Divider,
    Page,
    Text,
    alignment,
)

logger = logging.getLogger(__name__)


class BaseTabBodyView(Column):
    """
    タブのボディ部分の基底クラス
    """
    def __init__(self, page: Page, title: str):
        super().__init__(
            spacing=10,
            expand=True,
            alignment=alignment.center,
        )
        self.page = page
        self.title = title

        self.controls = [
            Container(
                padding=10,
                alignment=alignment.center,
                content=Text(title, size=30),
            ),
            Divider(),
            self.create_body(),
        ]

    def create_body(self):
        """サブクラスで具体的なコントロールを実装"""
        return Column(
            controls=[
                Text(
                    "No settings available for this tab",
                    size=20,
                    #  alignment=alignment.center,
                    color="yellow",
                ),
            ]
        )
