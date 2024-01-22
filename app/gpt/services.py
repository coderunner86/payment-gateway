import requests
from fastapi import HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from app.helpers.session import get_user_id_from_session
load_dotenv() 

class UserQuestion(BaseModel):
    question: str
    gptResponse: str
    userId: int    


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

    async def create_question(self, request: Request,user_question: UserQuestion):
        try:
            session_id = request.cookies.get("session_id")
            print("session_id", session_id)
            user_id = get_user_id_from_session(session_id)
            print("user_id", user_id)
            gpt_response = self.ask_gpt(user_question.question)
            print("gpt_response", gpt_response)
            data = {"question": user_question.question, "gpt_response": user_question.gptResponse, "user_id": user_id}
            print("data", data)
            result = await self.repository.user_question.create(data=data)
            print("result", result)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))