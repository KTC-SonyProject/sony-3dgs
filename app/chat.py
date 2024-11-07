import flet as ft

from app.ai.agent import ChatbotGraph


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


# アイコン、名前、チャットの再利用可能なチャットメッセージ
class ChatMessage(ft.Row):
    def __init__(self, message:Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            # アイコン
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name)
            ),
            # 名前とメッセージのカラム
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True)
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
    def get_avatar_color(self, user_name: str) -> ft.colors:
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]

        return colors_lookup[hash(user_name) % len(colors_lookup)]


chatbot_graph = ChatbotGraph(verbose=True)


def main(page: ft.Page) -> None:
    page.title = 'AIチャット'

    # 送られてきたメッセージをchatに追加
    def on_message(message: Message) -> None:
        m = ChatMessage(message)
        chat.controls.append(m)
        page.update()

    # メッセージの送信
    def send_message_click(e: ft.ControlEvent) -> None:
        if new_message.value != "":
            on_message(Message(user_name='user', text=new_message.value, message_type='human'))
            send_message = new_message.value
            new_message.value = ''
            progress.visible = True
            page.update()

            for response in chatbot_graph.stream_graph_updates(send_message):
                on_message(Message(user_name='AI', text=response, message_type='ai'))

            progress.visible = False
            new_message.focus()
            page.update()

    # スクロールをつける
    chat = ft.ListView(
        expand = True,
        spacing = 10,
        auto_scroll = True
    )

    # メッセージボックス
    new_message = ft.TextField(
        hint_text = "Write a message...",
        autocorrect = True,
        shift_enter = True,
        min_lines = 1,
        max_lines = 5,
        filled = True,
        expand = True,
        on_submit = send_message_click
    )

    # プログレスバー
    progress = ft.ProgressBar(
        color = ft.colors.PINK, # 進むバーの色
        bgcolor = ft.colors.GREY_200, # バーの背景色
        visible = False # 非表示にする
    )

    # ページに表示
    page.add(
        ft.Container(
            content = chat,
            border = ft.border.all(1, ft.colors.OUTLINE),
            border_radius = 5,
            padding = 10,
            expand = True,
        ),
        progress,
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon = ft.icons.SEND_ROUNDED,
                    tooltip = "Send message",
                    on_click = send_message_click
                )
            ]
        )
    )

ft.app(main)
