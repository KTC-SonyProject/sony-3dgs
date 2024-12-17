# postgresqlとの接続を行うモジュール
import logging
import sqlite3
from pathlib import Path

from psycopg_pool import ConnectionPool

from app.controller.settings_manager import SettingsManager

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, settings_manager: SettingsManager):
        """
        データベース接続情報を初期化するクラス
        :param settings: 設定辞書 (PostgreSQL/SQLite両対応)
        :param use_connection_kwargs: PostgreSQLで接続パラメータを追加するか
        """
        self.settings_manager = settings_manager
        self.use_postgres = self.settings_manager.get_setting("database_settings.use_postgres")

        if self.use_postgres:
            self._init_postgres()
        else:
            self._init_sqlite()

    def get_nested_setting(self, nested_key: str, key: str):
        """
        ネストされた設定を取得する
        :param nested_key: ネストされた設定のキー
        :param key: ネストされた設定のキー
        :return: ネストされた設定の値
        """
        return self.settings_manager.get_setting(f"{nested_key}.{key}")

    def _init_postgres(self):
        """PostgreSQLデータベースに接続するための初期化を行う"""
        nested_key = "database_settings.postgres_settings"
        db_uri = (
            f"postgresql://"
            f"{self.get_nested_setting(nested_key, 'user')}:{self.get_nested_setting(nested_key, 'password')}"
            f"@{self.get_nested_setting(nested_key, 'host')}:{self.get_nested_setting(nested_key, 'port')}"
            f"/{self.get_nested_setting(nested_key, 'database')}?sslmode=disable"
        )
        self.pool = ConnectionPool(conninfo=db_uri, max_size=20, open=True)
        logging.info("PostgreSQL connection pool is initialized.")

    def _init_sqlite(self):
        """SQLiteデータベースに接続するための初期化を行う"""
        nested_key = "database_settings.sqlite_settings"
        database_path = self.get_nested_setting(nested_key, "database")
        # sqliteのファイルが存在しない場合は作成
        if not Path(database_path).exists():
            Path(database_path).touch()
            # init_sqlファイルを使用してテーブルを作成
            with sqlite3.connect(database_path) as connection:
                with open("db/sqlite/init/1_init.sql") as f:
                    connection.executescript(f.read())
            logging.info("SQLite database is created.")

        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        logging.info("SQLite connection is initialized.")

    def execute_query(self, query, params=None):
        """
        クエリを実行する（データ挿入や更新などの変更系）
        """
        try:
            if self.use_postgres:
                with self.pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        conn.commit()
                        logger.info("Query executed successfully (PostgreSQL).")
            else:
                query = query.replace("%s", "?")
                cursor = self.connection.cursor()
                cursor.execute(query, params or [])
                self.connection.commit()
                logger.info("Query executed successfully (SQLite).")
                # self.close_connection()
        except Exception as error:
            logger.error(f"Error executing query: {error}")

    def fetch_query(self, query, params=None) -> list:
        """
        クエリを実行し結果を取得する（データ取得系）
        """
        try:
            if self.use_postgres:
                with self.pool.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        result = cursor.fetchall()
                        logger.info("Query fetched successfully (PostgreSQL).")
                        return result
            else:
                query = query.replace("%s", "?")
                cursor = self.connection.cursor()
                cursor.execute(query, params or [])
                result = cursor.fetchall()
                logger.info("Query fetched successfully (SQLite).")
                # self.close_connection()
                return result
        except Exception as error:
            logger.error(f"Error fetching query: {error}")
            raise error

    def close_connection(self):
        """
        データベース接続を閉じる
        """
        if self.use_postgres:
            self.pool.close()
            logger.info("PostgreSQL connection pool is closed.")
        elif self.connection:
            self.connection.close()
            logger.info("SQLite connection is closed.")


if __name__ == "__main__":
    settings_manager = SettingsManager()
    db = DatabaseHandler(settings_manager)
    result = db.fetch_query("SELECT * FROM documents;")
    print(result)

    # IDが1のドキュメントを取得
    print("\n-----------------\n")
    result = db.fetch_query("SELECT * FROM documents WHERE document_id = %s;", (1,))
    print(result)

    db.close_connection()
