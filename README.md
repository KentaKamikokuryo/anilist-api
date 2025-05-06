# Anilist API Test

Anilist API を試行してみるための repo です。

## 概要

このプロジェクトは [Anilist GraphQL API](https://anilist.co/graphql) を使用して、アニメやマンガの情報を取得するためのシンプルなクライアントを提供します。認証なしで基本的な API 機能をテストすることができます。

## 機能

- アニメの詳細情報の取得（ID 指定）
- キーワードによるアニメ検索
- シーズン別アニメの取得
- 結果の整形表示

## 環境構築

### 前提条件

- Python 3.8 以上
- [Pyenv](https://github.com/pyenv/pyenv)（Python バージョン管理）
- [Poetry](https://python-poetry.org/)（依存関係管理）

### セットアップ手順

1. Pyenv で Python バージョンを設定

```bash
# 最新の Python をインストール（既にインストール済みの場合はスキップ）
pyenv install 3.11.4

# プロジェクトディレクトリで使用する Python バージョンを設定
pyenv local 3.11.4
```

2. Poetry で依存関係をインストール

```bash
# 依存関係をインストール
poetry install
```

## 使用方法

このプロジェクトには以下のスクリプトが含まれています：

1. **main.py** - 基本的な API 機能のデモ
2. **show_available_keys.py** - API から取得できるデータの構造を表示
3. **examples.py** - 様々な API 使用例を提供
4. **custom_query.py** - カスタム GraphQL クエリを実行するためのツール

### 基本的な使い方

```bash
# 基本的な API 機能のデモを実行
poetry run python main.py

# 利用可能なデータ構造を確認
poetry run python show_available_keys.py

# 様々な API 使用例を実行
poetry run python examples.py

# カスタムクエリを実行（引数なしで実行するとヘルプが表示されます）
poetry run python custom_query.py
```

### main.py

基本的な API 機能のデモを提供します：

1. 特定のアニメ（鬼滅の刃）の詳細情報を取得
2. キーワード「Attack on Titan」でアニメを検索
3. 2023年冬アニメのリストを取得

`main.py` を編集することで、異なるアニメ ID、検索キーワード、シーズンなどを指定できます：

```python
# 例：ワンピースの情報を取得（ID: 21）
display_anime_details(client, 21)

# 例：「Naruto」で検索
search_anime_by_keyword(client, "Naruto")

# 例：2023年春アニメを取得
get_seasonal_anime(client, 2023, "SPRING")
```

### show_available_keys.py

Anilist API から取得できるデータの構造を表示します。このスクリプトを実行すると：

1. アニメ詳細情報の構造
2. 検索結果の構造
3. シーズン別アニメの構造

が表示されます。API から取得できる情報の全体像を把握するのに役立ちます。

### examples.py

様々な API 使用例を提供します：

1. **基本的なアニメ情報の取得** - タイトル、エピソード数、ジャンルなど
2. **アニメのキャラクター情報の取得** - キャラクター名、役割、声優など
3. **スタジオ作品の取得** - 特定のスタジオが制作したアニメ一覧
4. **シーズン別ランキングの取得** - 特定のシーズンの人気アニメ
5. **ジャンルとタグによるアニメの取得** - 特定のジャンルとタグを持つアニメ

これらの例を参考に、独自のクエリを作成することができます。

### custom_query.py

カスタム GraphQL クエリを実行するためのコマンドラインツールです。このスクリプトを使用すると、独自の GraphQL クエリを実行し、結果を取得することができます。

使用例：

```bash
# 直接クエリを指定して実行
poetry run python custom_query.py --query '{ Media(id: 1) { id title { romaji } } }'

# ファイルからクエリを読み込んで実行
poetry run python custom_query.py --file query_examples/anime_details.graphql

# 変数を指定してクエリを実行
poetry run python custom_query.py --query 'query ($id: Int) { Media(id: $id) { id title { romaji } } }' --variables '{"id": 1}'

# 結果をファイルに保存
poetry run python custom_query.py --file query_examples/anime_details.graphql --variables '{"id": 1}' --output results.json
```

#### クエリ例

`query_examples` ディレクトリには、以下のようなクエリ例が含まれています：

1. **anime_details.graphql** - アニメの詳細情報を取得するクエリ
   ```bash
   poetry run python custom_query.py --file query_examples/anime_details.graphql --variables '{"id": 1}'
   ```

2. **search_anime.graphql** - アニメを検索するクエリ
   ```bash
   poetry run python custom_query.py --file query_examples/search_anime.graphql --variables '{"search": "鬼滅の刃", "page": 1, "perPage": 5}'
   ```

3. **character_info.graphql** - キャラクター情報を取得するクエリ
   ```bash
   poetry run python custom_query.py --file query_examples/character_info.graphql --variables '{"search": "Levi"}'
   ```

4. **seasonal_anime.graphql** - シーズン別アニメを取得するクエリ
   ```bash
   poetry run python custom_query.py --file query_examples/seasonal_anime.graphql --variables '{"season": "WINTER", "seasonYear": 2023}'
   ```

また、`query_examples/variables.json` ファイルには、各クエリで使用できる変数の例が含まれています：

```bash
# 変数ファイルを使用してクエリを実行
poetry run python custom_query.py --file query_examples/anime_details.graphql --variables-file query_examples/variables.json
```

このツールを使用すると、GraphQL クエリの実験や、特定のデータの取得が簡単に行えます。

## API クライアントの使い方

`anilist_client.py` には `AnilistClient` クラスが定義されており、独自のスクリプトで以下のように使用できます：

```python
from anilist_client import AnilistClient

# クライアントのインスタンスを作成
client = AnilistClient()

# アニメ情報を取得（ID指定）
result = client.get_anime_by_id(21)  # ワンピース

# キーワードでアニメを検索
result = client.search_anime("Naruto", page=1, per_page=10)

# シーズン別アニメを取得
result = client.get_seasonal_anime(2023, "SPRING", page=1, per_page=10)
```

## 参考リンク

- [Anilist API ドキュメント](https://anilist.gitbook.io/anilist-apiv2-docs/)
- [GraphQL 入門](https://graphql.org/learn/)
- [Anilist GraphQL API エクスプローラー](https://anilist.co/graphiql)
