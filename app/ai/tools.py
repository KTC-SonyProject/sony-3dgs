from langchain_core.documents import Document
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.ai.vector_db import get_vector_store


class SearchDocumentInput(BaseModel):
    query: str = Field(description="ドキュメントを検索するクエリ")

@tool("search_documents_tool", args_schema=SearchDocumentInput)
def search_documents(query: str) -> list[Document]:
    """
    ドキュメントを検索する関数
    """
    results = get_vector_store().similarity_search(
        query=query,
    )
    return results


tools = [search_documents]

if __name__ == "__main__":
    print(f"{search_documents.name=}, {search_documents.description=}, {search_documents.args=}")

    print(search_documents.invoke("test"))
