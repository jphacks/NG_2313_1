# jphacks2023_backend

## 概要
- このリポジトリは、JPHACKS2023のバックエンドのリポジトリです。

## 開発環境
- Python 3.10
- fastAPI 0.100.1

## Qdrantを落とす
- 以下のコマンドを実行してください。
```
docker pull qdrant/qdrant
docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

## 実行方法
- 以下のコマンドを実行してください。(.env.sampleを参考に.envを作成してください。
```
$ docker-compose up --build
```

## API docs
- 以下のURLにアクセスすると、APIのドキュメントが見れます。
```
http://localhost:8000/docs#/
```