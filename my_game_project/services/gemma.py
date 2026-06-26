# services/gemma.py
import os
from google import genai

class GemmaService:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        # 将来的にここで genai.Client(api_key=...) を初期化
        pass

    def request_raw_inference(self, prompt: str, system_instruction: str) -> str:
        """Gemma APIへ生のテキストリクエストを送信する最小単位の関数"""
        # TODO: 本番の実装をここに移送
        return "{}"
