import httpx
from fastapi import HTTPException, Request
from app.settings.database import database
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from app.helpers.session import get_user_id_from_session
load_dotenv()

class UserQuestion(BaseModel):
    question: str
    gptResponse: Optional[str] = None
    
API_KEY = os.getenv("API_KEY")

class GptService:
    def __init__(self):
        self.API_KEY = API_KEY
        self.repository = database

    async def ask_gpt(self, question: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
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
            except httpx.RequestError as e:
                raise HTTPException(status_code=400, detail=f"HTTP request failed: {e}")

    async def create_question(self, request: Request, userquestion: UserQuestion):
        try:
            session_id = request.cookies.get("session_id")
            user_id = get_user_id_from_session(session_id)
            data = userquestion.dict()
            
            # gpt_response = self.ask_gpt(self, userquestion.question)
                      
            result = await self.repository.userquestion.create(data=data) #.gpt.create(data=data)
            print("result", result)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating question: {e}")
