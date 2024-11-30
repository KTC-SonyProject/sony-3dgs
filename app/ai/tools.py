from enum import Enum

from langchain_core.documents import Document
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.ai.vector_db import get_vector_store
from app.db_conn import DatabaseHandler
from app.settings import load_settings


class SearchDocumentInput(BaseModel):
    query: str = Field(description="ドキュメントを検索するクエリ")

@tool("search_documents_tool", args_schema=SearchDocumentInput)
def search_documents_tool(query: str) -> list[Document]:
    """
    ドキュメントを検索する関数
    この関数で取得したドキュメントをユーザーに返す場合は"[参考にしたドキュメント](metadataのsourceに格納されている数値)"のような形で返す
    """
    results = get_vector_store().similarity_search(
        query=query,
    )
    # results = {
    #     "content": res["content"],
    # }
    return results


class OperationStr(Enum):
    next_scene = "次のシーン"
    previous_scene = "前のシーン"
    rotate_scene = "シーンを回転"


class DisplayOperationInput(BaseModel):
    operation: str = Field(
        description=(
            f"操作内容 操作は以下のいずれかの文字列で指定する: {', '.join([op.value for op in OperationStr])}"
        )
    )

@tool("display_operation_tool", args_schema=DisplayOperationInput)
def display_operation_tool(operation: str) -> str:
    """
    Displayの操作を行う関数
    """
    # TODO: ここにDisplayの操作を行うコードを記述する

    if operation == OperationStr.next_scene.value:
        # 次のシーンを表示する
        pass
    elif operation == OperationStr.previous_scene.value:
        # 前のシーンを表示する
        pass
    elif operation == OperationStr.rotate_scene.value:
        # シーンを回転する
        pass
    else:
        raise ValueError(f"Invalid operation: {operation}")

    return f"次の操作を行いました: {operation}"


tools = [search_documents_tool, display_operation_tool]

if __name__ == "__main__":
    print(f"{search_documents_tool.name=}, {search_documents_tool.description=}, {search_documents_tool.args=}")
    print(f"{display_operation_tool.name=}, {display_operation_tool.description=}, {display_operation_tool.args=}")


    # print(search_documents_tool.invoke("test"))
    print(display_operation_tool.invoke("次のシーン"))
