import os
from typing import Any

from langchain.globals import set_verbose
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from app.settings import load_settings


def llm_settings(verbose: bool = False) -> Any:
    set_verbose(verbose)
    settings = load_settings("llm_settings")
    if "azure" == settings.get("llm_provider"):
        settings = settings.get("azure_llm_settings")
        # 変数が空文字の場合はエラーを出す
        for key in settings:
            print(settings[key])
            if settings[key] == "":
                raise ValueError(f"Invalid setting: {key}")
        os.environ["AZURE_OPENAI_ENDPOINT"] = settings.get("endpoint")
        os.environ["AZURE_OPENAI_API_KEY"] = settings.get("api_key")
        return AzureChatOpenAI(
            deployment_name=settings.get("deployment_name"),
            api_version=settings.get("api_version"),
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            streaming=True,
        )
    elif "gemini" == settings.get("llm_provider"):
        print("Gemini is not implemented yet.")
        raise ValueError(f"Invalid LLM type: {settings.get("llm_provider")}")
    elif "ollama" == settings.get("llm_provider"):
        print("Ollama is not implemented yet.")
        raise ValueError(f"Invalid LLM type: {settings.get("llm_provider")}")
    else:
        raise ValueError(f"Invalid LLM type: {settings.get("llm_provider")}")

def embedding_model_settings():
    settings = load_settings("llm_settings")
    if "azure" == settings.get("embedding_provider"):
        settings = settings.get("azure_llm_settings")
        os.environ["AZURE_API_KEY"] = settings.get("api_key")
        return AzureOpenAIEmbeddings(
            azure_endpoint=settings.get("endpoint"),
            azure_deployment=settings.get("deployment_embdding_name"),
            openai_api_version=settings.get("api_version"),
        )
    else:
        raise ValueError(f"Invalid embedding model type: {settings.get("embedding_provider")}")


if __name__ == "__main__":
    llm = llm_settings(verbose=True)
    print(llm.invoke("こんにちは、世界！"))
