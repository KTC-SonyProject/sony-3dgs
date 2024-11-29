import os
from typing import Any

from langchain.globals import set_verbose
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from app.settings import load_settings


def llm_settings(verbose: bool = False) -> Any:
    set_verbose(verbose)
    config = load_settings("llm_config")
    if "azure" == config.get("llm_provider"):
        config = config.get("azure_llm_config")
        os.environ["OPENAI_ENDPOINT"] = config.get("endpoint")
        os.environ["OPENAI_API_KEY"] = config.get("api_key")
        return AzureChatOpenAI(
            azure_deployment=config.get("deployment_name"),
            api_version=config.get("api_version"),
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            streaming=True,
        )
    elif "ollama" == config.get("llm_provider"):
        print("Ollama is not implemented yet.")
        raise ValueError(f"Invalid LLM type: {config.get("llm_provider")}")
    else:
        raise ValueError(f"Invalid LLM type: {config.get("llm_provider")}")

def embedding_model_settings():
    config = load_settings("llm_config")
    if "azure" == config.get("embedding_provider"):
        config = config.get("azure_llm_config")
        os.environ["AZURE_API_KEY"] = config.get("api_key")
        return AzureOpenAIEmbeddings(
            azure_endpoint=config.get("endpoint"),
            azure_deployment=config.get("deployment_embdding_name"),
            openai_api_version=config.get("api_version"),
        )
    else:
        raise ValueError(f"Invalid embedding model type: {config.get("embedding_provider")}")


if __name__ == "__main__":
    llm = llm_settings(verbose=True)
    print(llm.invoke("こんにちは、世界！"))
