import logging

from flet import (
    AlertDialog,
    ButtonStyle,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    Divider,
    ElevatedButton,
    FloatingActionButton,
    IconButton,
    Icons,
    InputBorder,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Page,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    TextField,
    TextOverflow,
    VerticalDivider,
    alignment,
    border_radius,
    padding,
)

from app.ai.vector_db import delete_document_from_vectorstore, indexing_document
from app.viewmodels.documents_manager import DocumentsManager

logger = logging.getLogger(__name__)

class RailDescription(Row):
    def __init__(self, page: Page, title: str, id: int):
        super().__init__()
        self.page = page
        self.title = title
        self.id = id
        # self.expand = True
        self.alignment = MainAxisAlignment.SPACE_BETWEEN

        self.controls = [
            Text(self.title, width=150, max_lines=1, overflow=TextOverflow.ELLIPSIS),
            IconButton(icon=Icons.EDIT_NOTE, tooltip="Edit Documents", on_click=self.click),
        ]

    def click(self, e):
        self.page.go(f"/documents/{self.id}/edit")


class Sidebar(Container):
    def __init__(self, page: Page, docs_manager: DocumentsManager):
        super().__init__()
        self.page = page
        self.docs_manager = docs_manager

        self.nav_rail_visible = True
        self.nav_rail_items = []

        documents_list = self.docs_manager.get_all_documents()
        for document in documents_list:
            self.nav_rail_items.append(
                NavigationRailDestination(
                    label_content=RailDescription(self.page, document["title"], document["id"]),
                    label=document["title"],
                    selected_icon=Icons.CHEVRON_RIGHT_ROUNDED,
                    icon=Icons.CHEVRON_RIGHT_OUTLINED,
                    data=document["id"],
                )
            )

        # sidebarのおおもとの設定
        self.nav_rail = NavigationRail(
            selected_index=None,
            label_type=NavigationRailLabelType.ALL,
            # min_width=100,
            leading=FloatingActionButton(icon=Icons.CREATE, text="ADD DOCUMENT", on_click=self.open_modal),
            group_alignment=-0.9,
            destinations=self.nav_rail_items,
            on_change=self.tap_nav_icon,
            expand=True,
            extended=True,
        )
        # sidebarの表示切り替えボタン
        self.toggle_nav_rail_button = IconButton(
            icon=Icons.ARROW_CIRCLE_LEFT,
            icon_color=Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
            tooltip="Collapse Nav Bar",
        )
        self.visible = self.nav_rail_visible

        # ドキュメント追加モーダルの設定
        self.dlg_modal = AlertDialog(
            modal=True,
            inset_padding=padding.symmetric(vertical=40, horizontal=100),
            title=Text("新規追加"),
            content=TextField(
                label="タイトル名",
                border=InputBorder.UNDERLINE,
                filled=True,
                hint_text="Enter title name here",
            ),
            actions=[
                TextButton(text="Yes", on_click=self.modal_yes_action),
                TextButton(text="No", on_click=self.modal_no_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.content = Row(
            controls=[
                self.nav_rail,
                Container(
                    bgcolor=Colors.BLACK26,
                    border_radius=border_radius.all(30),
                    # height=480,
                    alignment=alignment.center_right,
                    width=2,
                ),
                self.toggle_nav_rail_button,
            ],
            vertical_alignment=CrossAxisAlignment.START,
        )

    def toggle_nav_rail(self, e):
        self.nav_rail.visible = not self.nav_rail.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.toggle_nav_rail_button.tooltip = (
            "Open Side Bar" if self.toggle_nav_rail_button.selected else "Collapse Side Bar"
        )
        self.update()

    def tap_nav_icon(self, e):
        selected_index = e.control.selected_index
        document_id = e.control.destinations[selected_index].data
        self.page.go(f"/documents/{document_id}")

    def open_modal(self, e):
        e.control.page.overlay.append(self.dlg_modal)
        self.dlg_modal.open = True
        e.control.page.update()

    def modal_yes_action(self, e):
        try:
            title = self.dlg_modal.content.value
            if not title:
                logger.warning("タイトル名が入力されていません")
                raise Exception("タイトル名が入力されていません")
            # self.db.execute_query(
            #     "INSERT INTO documents (title, content) VALUES (%s, %s)", (self.dlg_modal.content.value, "")
            # )
            # result = self.db.fetch_query("SELECT document_id FROM documents ORDER BY created_at DESC LIMIT 1;")
            # print(result)
            # self.dlg_modal.open = False
            # self.page.go(f"/documents/{result[0][0]}/edit")
            document_id = self.docs_manager.add_document(title)
            logger.debug(f"Document added: {document_id=}, {title=}")
            self.dlg_modal.open = False
            self.page.go(f"/documents/{document_id}/edit")
        except Exception as error:
            logger.error(f"Error adding document: {error}")
            self.dlg_modal.content.error_text = str(error)
            e.control.page.update()

    def modal_no_action(self, e):
        self.dlg_modal.open = False
        e.control.page.update()


class DocumentBody(Container):
    def __init__(self, page: Page, content: str = ""):
        super().__init__()
        self.page = page
        self.expand = True
        self.alignment = alignment.top_left
        # self.spacing = 10
        self.content_value = content

        self.content = Column(
            controls=[
                Markdown(
                    value=self.content_value,
                    selectable=True,
                    extension_set=MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: self.page.launch_url(e.data),
                ),
            ],
            scroll="hidden",
        )


class DocumentsView(Row):
    def __init__(self, page: Page, docs_manager: DocumentsManager, document_id: int = 0):
        super().__init__()
        self.page = page
        self.docs_manager = docs_manager

        self.expand = True
        self.vertical_alignment = CrossAxisAlignment.START

        self.documents_list = self.docs_manager.get_all_documents()

        if document_id == 0:
            self.controls = [
                Sidebar(self.page, docs_manager=self.docs_manager),
                Text("test."),
            ]
        else:
            document = self.docs_manager.get_document_by_id(document_id)
            content = document["content"] if document else "Document not found."
            self.controls = [
                Sidebar(self.page, docs_manager=self.docs_manager),
                DocumentBody(self.page, content=content),
            ]


class EditBody(Row):
    def __init__(self, page: Page, docs_manager: DocumentsManager, document_id: int):
        super().__init__()
        self.page = page
        self.docs_manager = docs_manager
        self.document_id = document_id

        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True

        document = self.docs_manager.get_document_by_id(document_id)
        self.document_title = document["title"] if document else "Untitled"
        self.document_content = document["content"] if document else ""

        self.text_field = TextField(
            value=self.document_content,
            multiline=True,
            expand=True,
            border_color=Colors.TRANSPARENT,
            on_change=self.update_preview,
            hint_text="Document here...",
        )
        self.document_body = DocumentBody(self.page, content=self.text_field.value)

        self.controls = [
            self.text_field,
            VerticalDivider(color=Colors.BLUE_GREY_400),
            self.document_body,
        ]

    def update_preview(self, e):
        # self.document_body.content_value = self.text_field.value
        self.document_body.content.controls[0].value = self.text_field.value
        self.document_body.update()
        self.update()
        self.page.update()


class EditDocumentsView(Column):
    def __init__(self, page: Page, docs_manager: DocumentsManager, document_id: int):
        super().__init__()
        self.page = page
        self.docs_manager = docs_manager
        self.document_id = document_id

        self.expand = True
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.spacing = 10

        document = self.docs_manager.get_document_by_id(document_id)
        self.document_title = document["title"] if document else "Untitled"
        self.document_content = document["content"] if document else ""

        self.dlg_modal = AlertDialog(
            title=Text("※注意※", color=Colors.RED),
            modal=True,
            content=Text("ドキュメントの変更内容を保存せずに戻りますか？"),
            actions=[
                ElevatedButton(
                    text="保存して戻る",
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(radius=10),
                    ),
                    on_click=self.save_document,
                ),
                TextButton(text="保存せずに戻る", on_click=self.modal_yes_action),
                TextButton(text="変更を続ける", on_click=self.modal_no_action),
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        self.edit_body = EditBody(self.page, self.docs_manager, self.document_id)
        self.title_field = TextField(
            value=self.document_title,
            border=InputBorder.UNDERLINE,
        )

        self.controls = [
            Row(
                controls=[
                    Row(
                        controls=[
                            IconButton(icon=Icons.ARROW_BACK, on_click=self.open_modal, tooltip="Back"),
                            self.title_field,
                        ],
                    ),
                    Row(
                        controls=[
                            TextButton(text="Save", on_click=self.save_document, icon=Icons.SAVE),
                            TextButton(text="Delete", on_click=self.delete_document, icon=Icons.DELETE),
                        ],
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            Divider(color=Colors.BLUE_GREY_400),
            self.edit_body,
        ]

    def back_page(self, e):
        self.page.go(f"/documents/{self.document_id}")

    def save_document(self, e):
        title = self.title_field.value
        content = self.edit_body.text_field.value
        self.docs_manager.update_document(self.document_id, title, content)
        indexing_document(content, self.document_id)
        self.back_page(e)

    def delete_document(self, e):
        self.docs_manager.delete_document(self.document_id)
        delete_document_from_vectorstore(self.document_id)
        self.page.go("/documents")

    def open_modal(self, e):
        self.page.overlay.append(self.dlg_modal)
        self.dlg_modal.open = True
        self.page.update()

    def modal_yes_action(self, e):
        self.dlg_modal.open = False
        self.back_page(e)

    def modal_no_action(self, e):
        self.dlg_modal.open = False
        self.page.update()
