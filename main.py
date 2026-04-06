from fastapi import FastAPI # FastAPIの読み込み
from pydantic import BaseModel  # 型定義のためのクラス
import anthropic # AIは今回anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()  # .envを読み込む

app = FastAPI()

# ── リクエストの型定義 ──────────────────────────
# Railsのストロングパラメーターに相当
# これを定義するだけでバリデーションが自動でかかる✨
class RecommendRequest(BaseModel):
    game_title: str      # 必須・文字列
    review: str = ""     # 任意・デフォルトは空文字

# Railsのcurrent_userの名前を受け取りますわ
class FortuneRequest(BaseModel):
    game_title: str      # 必須・文字列
    user_name: str       # Railsのcurrent_user.nameを渡しますの

# ── エンドポイント ──────────────────────────────
# POSTリクエストを受け取る
@app.post("/api/recommend")
def recommend_game(request: RecommendRequest):
    
    # Claudeクライアントを初期化（API KEYは自動で.envから読む）
    client = anthropic.Anthropic()

    # ── プロンプト（命令文）を組み立て ──
    prompt = f"""
    ユーザーが「{request.game_title}」というゲームをプレイしました。
    感想: {request.review}

    このゲームを楽しんだユーザーに、次にプレイするゲームを3本おすすめしてください。
    それぞれ50文字以内で理由も添えてください。
    RPGのゲームの占いオババの口調で答えてください。
    必ずJSON形式のみで返してください。マークダウンのコードブロックは不要です。
    {{"recommendations": [{{"title": "ゲーム名", "reason": "理由"}}]}}
    """

    # ── Claude APIをここで呼ぶ ──
    # client.messages.create → HTTPのPOSTリクエストを内部で実行
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # ── AIからの返答の処理──
    # message.content[0].text にClaudeの返答が入る
    return {
        "game_title": request.game_title,
        "result": json.loads(message.content[0].text)  # 文字列→JSONに変換
    }

# ── 占いエンドポイント ──────────────────────────
# ゲームタイトルとユーザー名を受け取って相性を占うエンドポイント

@app.post("/api/fortune")
def fortune(request: FortuneRequest):

    client = anthropic.Anthropic()

    # ── プロンプトを組み立て ──
    prompt = f"""
    あなたはRPGの世界に住む神秘的な占い師です。
    {request.user_name}さんは「{request.game_title}」というゲームをプレイしました。
    次に運命づけられているゲームを3本、占い師らしい神秘的な口調で紹介してください。

    必ずJSON形式のみで返してください。マークダウンのコードブロックは不要です。
    {{
      "predictions": [
        {{
          "title": "ゲームタイトル",
          "message": "占い師口調で60文字程度のおすすめメッセージ"
        }}
      ]
    }}
    """

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)
