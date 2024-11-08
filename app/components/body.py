from flet import (
    Column,
    Text,
)


class ContentBody(Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Text('**********************'),
            Text('This is Main Body.'),
            Text('**********************'),
        ]
