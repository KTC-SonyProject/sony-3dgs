from flet import (
    Column,
    Text,
)


class ContentBody(Column):
    def __init__(self, text:str='Body Text'):
        super().__init__()
        self.text = text
        self.spacing = 10
        self.controls = [
            Text('**********************'),
            Text(self.text),
            Text('**********************'),
        ]
