from flet import (
    Column,
    Text,
)


class DocumentsBody(Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Text('**********************'),
            Text('Documents Body'),
            Text('**********************'),
        ]
