# jphacks2023_backend

## 概要
- このリポジトリは、JPHACKS2023のバックエンドのリポジトリです。

## 実行方法
実行時.envで設定をする必要があります
### OpenAPIのキーの発行方法
  [OpenAIキー発行ページ](https://platform.openai.com/account/api-keys)

1. リンクにアクセス 
2. 2Create a new API keyをクリック 
3. API key nameに任意の名前を入力  
4. Create secret keyを作成 
5. .envに以下のように記述
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

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