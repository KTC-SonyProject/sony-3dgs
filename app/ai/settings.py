import os
from typing import Any

from dotenv import load_dotenv
from langchain.globals import set_verbose
from langchain_openai import AzureChatOpenAI

load_dotenv()

# class LLMSettings:
#     """
#     このクラスは、言語モデルの設定を管理します。
#     """
#     def __init__(self, llm_type: str = "AzureChatOpenAI", verbose: bool = False):
#         self.verbose = verbose

#         if llm_type == "AzureChatOpenAI":
#             self.llm = AzureChatOpenAI(
#                 azure_deployment=os.environ['AZURE_DEPLOYMENT_NAME'],
#                 api_version=os.environ['OPENAI_API_VERSION'],
#                 temperature=0,
#                 max_tokens=None,
#                 timeout=None,
#                 max_retries=2,
#                 verbose=self.verbose
#             )
#         elif llm_type == "Ollama":
#             print("Ollama is not implemented yet.")
#         else:
#             raise ValueError(f"Invalid LLM type: {llm_type}")

#     def __getattr__(self, name: str) -> Any:
#         return getattr(self.llm, name)

def llm_settings(llm_type: str = "AzureChatOpenAI", verbose: bool = False) -> Any:
    set_verbose(verbose)
    if llm_type == "AzureChatOpenAI":
        return AzureChatOpenAI(
            azure_deployment=os.environ['AZURE_DEPLOYMENT_NAME'],
            api_version=os.environ['OPENAI_API_VERSION'],
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            streaming=True,
        )
    elif llm_type == "Ollama":
        print("Ollama is not implemented yet.")
        raise ValueError(f"Invalid LLM type: {llm_type}")
    else:
        raise ValueError(f"Invalid LLM type: {llm_type}")

if __name__ == "__main__":
    llm = llm_settings(verbose=True)
    print(llm.invoke("こんにちは、世界！"))
