-- 作成したDBに接続
\c main_db;

-- ドキュメントテーブル作成
DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
	document_id SERIAL PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	content TEXT,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
