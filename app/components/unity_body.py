import logging
import os

from flet import (
    Column,
    Container,
    ElevatedButton,
    FilePicker,
    FilePickerUploadFile,
    Page,
    Row,
    Tab,
    TabAlignment,
    Tabs,
    Text,
    alignment,
)

logger = logging.getLogger(__name__)

class DisplaySettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.spacing = 10
        self.controls = [
            Text("**********************"),
            Text("Display Settings Body"),
            Text("**********************"),
        ]


class FileSettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 10
        self.file_picker = FilePicker(on_result=self.on_file_result, on_upload=self.on_file_upload)
        self.page.overlay.append(self.file_picker)
        self.selected_files = Text("No files selected")

        self.controls = [
            Text("**********************"),
            Text("File Settings Body"),
            Text("**********************"),
            ElevatedButton(
                text="ファイルを選択",
                on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["txt", "pdf", "obj", "ply"]),
            ),
            self.selected_files,
            ElevatedButton(
                visible=False,
                text="ファイルをアップロード",
                on_click=self.upload_files,
            )
        ]

    def on_file_result(self, e):
        logger.debug(f"ファイルが選択されました: {e.files}")
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "No files selected"
        )
        self.controls[5].visible = True if e.files else False
        self.page.update()

    def upload_files(self, e):
        logger.debug(f"ファイルをアップロードします: {self.file_picker.result.files}")
        upload_list = []
        try:
            if self.file_picker.result is not None and self.file_picker.result.files is not None:
                for f in self.file_picker.result.files:
                    upload_list.append(
                        FilePickerUploadFile(
                            f.name,
                            upload_url=self.page.get_upload_url(f.name, 600),
                        )
                    )
                self.file_picker.upload(upload_list)
                # file_picker.upload() の処理の途中経過や完了は on_file_upload() で処理
        except Exception as error:
            logger.error(f"ファイルのアップロード中にエラーが発生しました: {error}")
            self.selected_files.value = "Error uploading files"
            self.controls[5].visible = False
            self.page.update()

    def on_file_upload(self, e):
        if e.progress == 1.0: # アップロードが完了した場合Unityにファイルを送信
            try:
                logger.debug("ファイルの一時アップロードが完了しました")
                # Unityにファイルを送信する
                file_path = f"{os.environ['FLET_ASSETS_DIR']}/uploads/{e.file_name}"
                result = self.page.data["server"].send_file(file_path)
                os.remove(file_path) # 一時ファイルを削除
                self.controls[5].visible = False
                self.page.update()
                logger.debug(f"ファイルのアップロードが完了しました\nunity message: {result}")
                self.selected_files.value = "ファイルのアップロードが完了しました"
                self.page.update()
            except ConnectionError as error:
                logger.error(f"Unityとの接続中にエラーが発生しました: {error}")
                os.remove(file_path) # 一時ファイルを削除
                self.selected_files.value = "送信先のUnityと接続できませんでした。"
                self.controls[5].visible = False
                self.page.update()
            except Exception as error:
                logger.error(f"ファイルのアップロード中にエラーが発生しました: {error}")
                self.selected_files.value = "Error uploading files"
                self.controls[5].visible = False
                self.page.update()

class TabBody(Tab):
    def __init__(self, page: Page, title: str):
        super().__init__()
        self.page = page
        self.text = title
        self.expand = True

        if title == "Display":
            self.content = DisplaySettingsBody(self.page)
        elif title == "File":
            self.content = FileSettingsBody(self.page)
        else:
            self.content = Text("No settings available for this tab")

class UnityBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 10
        self.expand = True
        self.controls = [
            Container(
                padding=10,
                alignment=alignment.center,
                content=Row(
                    spacing=20,
                    controls=[
                        Text("Unity Application", size=30),
                        # ElevatedButton("Save Settings", on_click=self.save_settings),
                    ],
                ),
            ),
            Tabs(
                expand=True,
                selected_index=0,
                animation_duration=300,
                tab_alignment=TabAlignment.CENTER,
                tabs=[
                    TabBody(page, "Display"),
                    TabBody(page, "File"),
                    TabBody(page, "Other"),
                ]
            ),
        ]
