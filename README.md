# chatgpt-python-lambda

## 概要

テキストから目次を検出し、JSON 形式で結果を返す。

```
出力例：
{
  "chapters": [
    {
      "title": "第1章: はじめに",
      "page": 1,
      "sections": [
        {
          "title": "1.1 背景",
          "page": 2
        },
        {
          "title": "1.2 目的",
          "page": 3
        }
      ]
    },
    {
      "title": "第2章: 方法",
      "page": 5,
      "sections": []
    }
  ]
}
```

## Docker イメージをビルドする

```
$ docker build -t toc .
```

## タグをつける

```
$ docker tag toc:latest ユーザー名.dkr.ecr.ap-northeast-1.amazonaws.com/toc-lambda:<タグ名>
```

## ECS にデプロイする

```
$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ユーザー名.dkr.ecr.ap-northeast-1.amazonaws.com
$ docker push ユーザー名.dkr.ecr.ap-northeast-1.amazonaws.com/toc:<タグ名>
```

## ローカルでデバッグ

コンテナを起動する

```
$ docker run --rm --publish 9000:8080 --name toc toc
```

curl でリクエストのテスト

```
$ curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{ "body": ... }'
```
