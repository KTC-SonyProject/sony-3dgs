import json

DEFAULT_SETTINGS = {
    "general_settings": {
        "app_name": "Spadge",
        "app_description": "",
    },
    "db_settings": {
        "use_postgres": False,
        "postgres_settings": {
            "host": "postgres",
            "port": 5432,
            "database": "main_db",
            "user": "postgres",
            "password": "postgres",
        },
        "sqlite_settings": {
            "database": "main_db.db"
        },
    },
    "llm_settings": {
        "llm_provider": "azure",
        "embedding_provider": "azure",
        "azure_llm_settings": {
            "endpoint": "",
            "api_key": "",
            "deployment_name": "",
            "deployment_embdding_name": "",
            "api_version": "",
        },
    },
}

def load_settings(return_custom: str = None):
    """設定をファイルから読み込む"""
    try:
        with open("local.settings.json") as f:
            settings = json.load(f)
        if return_custom:
            return settings.get(return_custom)
        return settings
    except FileNotFoundError:
        with open("local.settings.json", "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return settings
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}
