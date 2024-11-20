from flet import (
    Column,
    Page,
    Text,
)


class DocumentsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Text('**********************'),
            Text('Documents Body'),
            Text('**********************'),
        ]
