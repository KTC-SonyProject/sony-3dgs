-- ドキュメントテーブル作成
DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP,'localtime')),
    updated_at DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP,'localtime'))
);