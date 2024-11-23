from flet import (
    Column,
    Page,
    Text,
    Container,
    Markdown,
    MarkdownExtensionSet,
    Row,
    CrossAxisAlignment,
    IconButton,
    Icon,
    FloatingActionButton,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    alignment,
    colors,
    icons,
    border_radius,
    TextButton,
    padding,
    margin,
)

from app.db_conn import DatabaseHandler


class Sidebar(Container):
    def __init__(self, page:Page, documents_list: list):
        super().__init__()
        self.page = page
        self.nav_rail_visible = True
        self.documents_list = documents_list

        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("Boards"),
                label="Boards",
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED
            ),
            NavigationRailDestination(
                label_content=Text("Members"),
                label="Members",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),
        ]

        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            height=110
        )

        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,
            bgcolor=colors.BLUE_GREY,
        )
        self.get_document_rail()
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
            tooltip="Collapse Nav Bar",
        )

        self.content=Column(
            controls = [
                Row([
                    Text("Workspace"),
                ], alignment="spaceBetween"),
                # divider
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.top_nav_rail,
                # divider
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.bottom_nav_rail
            ],
            tight=True,
        ),
        self.padding=padding.all(15),
        self.margin=margin.all(0),
        self.width=250,
        #expand=True,
        self.bgcolor=colors.BLUE_GREY,
        self.visible=self.nav_rail_visible,

    def get_document_rail(self):
        self.bottom_nav_rail.destinations = []
        for document in self.documents_list:
            self.bottom_nav_rail.destinations.append(
                NavigationRailDestination(
                    label_content=Text(document[1]),
                    label=document[1],
                    icon=icons.BOOK_OUTLINED,
                    selected_icon=icons.BOOK_ROUNDED,
                )
            )

    def toggle_nav_rail(self, e):
        self.nav_rail.visible = not self.nav_rail.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.toggle_nav_rail_button.tooltip = (
            "Open Side Bar" if self.toggle_nav_rail_button.selected else "Collapse Side Bar"
        )
        self.update()

    def top_nav_change(self, e):
        index = e if (type(e) is int) else e.control.selected_index
        self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        self.update()
        if index == 0:
            self.page.route = "/boards"
        elif index == 1:
            self.page.route = "/members"
        self.page.update()

    def bottom_nav_change(self, e):
        index = e if (type(e) is int) else e.control.selected_index
        self.top_nav_rail.selected_index = None
        self.bottom_nav_rail.selected_index = index
        self.page.go(f"/documents/{index}")


class DocumentBody(Container):
    def __init__(self, page: Page, content: str = ""):
        super().__init__()
        self.page = page
        self.expand = True
        self.alignment=alignment.top_left
        self.spacing = 10

        self.content = Column(
            controls=[
                Markdown(
                    value=content,
                    selectable=True,
                    extension_set=MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: self.page.launch_url(e.data),
                ),
            ],
            scroll="hidden",
        )

class DocumentsBody(Row):
    def __init__(self, page: Page, document_id: int = 0):
        super().__init__()
        self.page = page
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True

        self.settings = self.page.data["settings"]()
        self.db = DatabaseHandler(self.settings)

        self.documents_list = self.get_document_list()

        if document_id == 0:
            self.controls = [
                Sidebar(self.page, documents_list=self.documents_list),
                Text("test."),
            ]
        else:
            self.document_body = self.get_document_body(document_id)
            content = self.document_body[2] if self.document_body else "Document not found."
            self.controls = [
                Sidebar(self.page, documents_list=self.documents_list),
                DocumentBody(self.page, content=content),
            ]

    def get_document_body(self, document_id: int):
        self.db.connect()
        result = self.db.fetch_query("SELECT * FROM documents WHERE document_id = %s", (document_id,))
        self.db.close_connection()
        return result[0] if result != [] else None

    def get_document_list(self):
        self.db.connect()
        result = self.db.fetch_query("SELECT document_id, title FROM documents;")
        self.db.close_connection()
        return result
