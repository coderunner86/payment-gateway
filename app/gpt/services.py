import httpx
from fastapi import HTTPException, Request
from app.settings.database import database
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from app.user.services import UserService
load_dotenv()

class UserQuestion(BaseModel):
    question: str
    userId: Optional[int] = None
    
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
            # Obtener el user_id de la sesión
            values = request.cookies.get("session_id")
            values = values.strip("() ")
            values = (values).split(",").pop(1)
            
            user_id = int(values)

            print("user_id", user_id)
           
            # Obtener la respuesta de GPT-3
            gptResponse = await self.ask_gpt(userquestion.question)
            data = userquestion.dict()
            
            data['userId'] = user_id  

            # Almacenar la pregunta 
            result = await self.repository.userquestion.create(data=data)
        
            find_the_user = await UserService().find_user(user_id=user_id)
            
            email = find_the_user.email
            name = find_the_user.name
            password = find_the_user.password
            gptResponse = gptResponse
    
            user_data={
                "name": name,
                "email": email,
                "password": password,
                "gptResponse": gptResponse
                }
            print("data_user", user_data)
            # Almacenar la respuesta 
            update_user = await self.repository.user.update(where={"id": user_id},
                data=user_data)
          
            return gptResponse
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating question: {e}")
