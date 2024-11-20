from flet import (
    Column,
    Markdown,
    MarkdownExtensionSet,
    Page,
    app,
)

# カレントディレクトリにあるREADME.mdを取得
md = open('README.md').read()


class TopBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Markdown(
                value=md,
                selectable=True,
                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                on_tap_link=lambda e: self.page.launch_url(e.data),
            )
        ]

if __name__ == '__main__':
    def main(page: Page) -> None:
        page.title = 'test app'
        page.scroll = "auto"
        chat_page = TopBody()
        page.add(chat_page)

    app(main)
