# postgresqlとの接続を行うモジュール
import logging

import psycopg2

from app.main import load_settings

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, settings: dict):
        """データベース接続情報を初期化する"""
        self.settings = settings
        self.use_postgres = settings.get("use_postgres", False)
        self.connection = None

    def connect(self):
        """PostgreSQLデータベースに接続する"""
        try:
            postgres_config = self.settings.get("postgres_config")
            self.connection = psycopg2.connect(**postgres_config)
            logger.info("Successfully connected to the PostgreSQL database.")
        except Exception as error:
            logger.error(f"Error connecting to PostgreSQL: {error}")
            self.connection = None

    def execute_query(self, query, params=None):
        """クエリを実行する（データ挿入や更新などの変更系）"""
        if self.connection is None:
            self.connect()
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self.connection.commit()
                    logger.info("Query executed successfully.")
            except Exception as error:
                logger.error(f"Error executing query: {error}")

    def fetch_query(self, query, params=None):
        """クエリを実行し結果を取得する（データ取得系）"""
        if self.connection is None:
            self.connect()
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
                    return result
            except Exception as error:
                logger.error(f"Error fetching query: {error}")
                return None

    def close_connection(self):
        """データベース接続を閉じる"""
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL connection is closed.")


if __name__ == '__main__':
    settings = load_settings()
    db = DatabaseHandler(settings)
    db.connect()
    result = db.fetch_query("SELECT * FROM documents;")
    print(result)
    db.close_connection()
