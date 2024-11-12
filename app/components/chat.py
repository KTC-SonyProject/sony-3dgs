from flet import (
    CircleAvatar,
    Column,
    Container,
    ControlEvent,
    IconButton,
    ListView,
    Page,
    ProgressBar,
    Row,
    Text,
    TextField,
    app,
    border,
    colors,
    icons,
)

from app.ai.agent import ChatbotGraph


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


# アイコン、名前、チャットの再利用可能なチャットメッセージ
class ChatMessage(Row):
    def __init__(self, message:Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            # アイコン
            CircleAvatar(
                content=Text(self.get_initials(message.user_name)),
                color=colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name)
            ),
            # 名前とメッセージのカラム
            Column(
                [
                    Text(message.user_name, weight="bold"),
                    Text(message.text, selectable=True)
                ],
                tight=True,
                spacing=5,
                expand=True
            )
        ]

    # ユーザ名の頭文字の取得
    def get_initials(self, user_name: str) -> str:
        return user_name[:1].capitalize()

    # ユーザ名に基づきハッシュを使いアイコンの色をランダムに決める
    def get_avatar_color(self, user_name: str) -> colors:
        colors_lookup = [
            colors.AMBER,
            colors.BLUE,
            colors.BROWN,
            colors.CYAN,
            colors.GREEN,
            colors.INDIGO,
            colors.LIME,
            colors.ORANGE,
            colors.PINK,
            colors.PURPLE,
            colors.RED,
            colors.TEAL,
            colors.YELLOW,
        ]

        return colors_lookup[hash(user_name) % len(colors_lookup)]




class ChatBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.chatbot_graph = ChatbotGraph(verbose=True)
        self.chat = ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message = TextField(
            hint_text="Write a message...",
            autocorrect=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=self.send_message_click
        )
        self.progress = ProgressBar(
            color=colors.PINK,
            bgcolor=colors.GREY_200,
            visible=False
        )
        self.controls = [
            Container(
                content=self.chat,
                border=border.all(1, colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True  # Containerも縦に展開する
            ),
            self.progress,
            Row(
                [
                    self.new_message,
                    IconButton(
                        icon=icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=self.send_message_click
                    )
                ]
            )
        ]
        self.expand = True

    def on_message(self, message: Message) -> None:
        m = ChatMessage(message)
        self.chat.controls.append(m)
        self.page.update()

    def send_message_click(self, e: ControlEvent) -> None:
        if self.new_message.value != "":
            self.on_message(Message(user_name='user', text=self.new_message.value, message_type='human'))
            send_message = self.new_message.value
            self.new_message.value = ''
            self.progress.visible = True
            self.page.update()

            for response in self.chatbot_graph.stream_graph_updates(send_message):
                self.on_message(Message(user_name='AI', text=response, message_type='ai'))

            self.progress.visible = False
            self.new_message.focus()
            self.page.update()


if __name__ == '__main__':
    def main(page: Page) -> None:
        page.title = 'AI Chat'
        chat_page = ChatBody(page)
        page.add(chat_page)

    app(main)
