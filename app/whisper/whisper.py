import os
import openai
from openai import AzureOpenAI
from app.settings import load_settings

client = AzureOpenAI(
        api_key=os.environ("AZURE_OPENAI_API_KEY"),  
        api_version="2024-02-01",
        azure_endpoint = os.environ("AZURE_OPENAI_ENDPOINT")
    )

class Whisper:
    def transcribe_audio(self):
        deployment_id = "あなたのデプロイメント名をここに入力してください"  # これは、モデルをデプロイしたときに選択したカスタム名に対応します。
        audio_test_file = "./input.wav" # ここに変換したい音声のパス
        
        result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),            
            model=deployment_id
        )
        return result