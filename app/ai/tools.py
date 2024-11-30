from langchain_core.documents import Document
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.ai.vector_db import get_vector_store
from app.db_conn import DatabaseHandler
from app.settings import load_settings


class SearchDocumentInput(BaseModel):
    query: str = Field(description="ドキュメントを検索するクエリ")

@tool("search_documents_tool", args_schema=SearchDocumentInput)
def search_documents(query: str) -> list[Document]:
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


tools = [search_documents]

if __name__ == "__main__":
    print(f"{search_documents.name=}, {search_documents.description=}, {search_documents.args=}")

    print(search_documents.invoke("test"))
