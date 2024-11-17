from flet import (
    Column,
    Markdown,
)

# カレントディレクトリにあるREADME.mdを取得
md = open('README.md').read()


class TopBody(Column):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Markdown(
                value=md,
                selectable=True,
                extension_set="gitHubWeb",
                on_tap_link=lambda e: self.page.launch_url(e.data),
            )
        ]
