import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("API_KEY")
class GptService:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def ask_gpt(self, question: str) -> str:
        try:
            response = requests.post(
                'https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions',
                headers={
                    'Authorization': f'Bearer {self.API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'prompt': question,
                    'temperature': 0.7,
                    'max_tokens': 60,
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['text']
        except requests.RequestException as e:
            raise HTTPException(status_code=400, detail=str(e))

    