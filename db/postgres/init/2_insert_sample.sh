# サンプルドキュメントの挿入
content=$(cat /docker-entrypoint-initdb.d/sample.md)
psql -d main_db -c "INSERT INTO documents (title, content) VALUES ('Sample Document1', '$content');"
psql -d main_db -c "INSERT INTO documents (title, content) VALUES ('Sample Document2', '$content');"