# 🔮 uranai_game

SaveData（ゲーム記録アプリ）のAIマイクロサービスです。  
プレイしたゲームタイトルをもとに、Claude APIが占い師口調で次のゲームを3本予言します。

## 概要

```
SaveData (Rails) → FastAPI → Claude API → JSONで返却
```

## 技術スタック

- Python 3.11
- FastAPI
- Anthropic Claude API
- Docker

## エンドポイント

| メソッド | パス             | 説明                                             |
| -------- | ---------------- | ------------------------------------------------ |
| POST     | `/api/fortune`   | ゲームタイトルをもとに次のゲームを占う           |
| POST     | `/api/recommend` | ゲームタイトルと感想をもとに次のゲームをおすすめ |

### リクエスト例

```bash
curl -X POST "http://localhost:8000/api/fortune" \
  -H "Content-Type: application/json" \
  -d '{"game_title": "ファイナルファンタジーVII", "user_name": "めたっぴ"}'
```

### レスポンス例

```json
{
  "predictions": [
    {
      "title": "風来のシレン",
      "message": "ふふふ…水晶玉に映るは千変万化の迷宮。同じ運命を紡ぐ風来人の姿が見えます。"
    }
  ]
}
```

## ローカル環境構築

```bash
# 仮想環境の作成・有効化
python3 -m venv venv
source venv/bin/activate

# ライブラリのインストール
pip install -r requirements.txt

# .envファイルを作成
echo "ANTHROPIC_API_KEY=your_api_key" > .env

# サーバー起動
uvicorn main:app --reload
```

## Docker（SaveDataと連携する場合）

SaveDataの `docker-compose.yml` に以下を追加します。

```yaml
ai_service:
  build: ../savedata_ai
  ports:
    - "8000:8000"
  env_file:
    - ../savedata_ai/.env
  volumes:
    - ../savedata_ai:/app
```

Rails側からは `http://ai_service:8000` で接続できます。

## 本番環境

Renderにデプロイしています。  
SaveData側の環境変数 `AI_SERVICE_URL` にデプロイ先のURLを設定しています。

## 関連リポジトリ

- [SaveData](https://github.com/Zundabyon/SaveData) - メインのRailsアプリ
