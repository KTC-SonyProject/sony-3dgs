-- DB作成
-- CREATE DATABASE main_db;
-- 作成したDBに接続
\c main_db;
-- テーブル作成
DROP TABLE IF EXISTS sample;
CREATE TABLE sample (
	id integer NOT NULL PRIMARY KEY,
	name char(100) NOT NULL,
	created_date_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- ID用シーケンス作成
CREATE SEQUENCE sample_id_seq START 1;
-- サンブルデータの登録
INSERT INTO sample (id, name) VALUES(nextval('sample_id_seq'), 'sample name');
