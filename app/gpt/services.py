import httpx
from fastapi import HTTPException, Request, Depends
from app.settings.database import database
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from app.helpers.session import get_user_id_from_session
from app.user.services import UserService, UpdateUser
load_dotenv()

class UserQuestion(BaseModel):
    question: str
    
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
            session_id = request.cookies.get("session_id")
            user_id = get_user_id_from_session(session_id)

            # Obtener la respuesta de GPT-3
            gptResponse = await self.ask_gpt(userquestion.question)
            # gpt_response = "hola"
            # Construir el diccionario de datos, incluyendo la respuesta de GPT-3
            data = userquestion.dict()
            
            # data['user_id'] = user_id  # Asegúrate de que tu modelo UserQuestion tenga este campo

            # Almacenar la pregunta y la respuesta en el repositorio
            result = await self.repository.userquestion.create(data=data)
            user_id=0
            find_the_user = await UserService().find_user(user_id=user_id)
            email = find_the_user.email
            name = find_the_user.name
            password = find_the_user.password
            gptResponse = gptResponse
            data_user = {
                "email": email,
                "name": name,
                "password": password,
                "gptResponse": gptResponse
            } 
            print("data_user", data_user)   
            update_user = await UpdateUser().update_user(user_id=user_id, user=data_user.items())
            # update_user = await UpdateUser().update_user(user_id=id, user=gptResponse)
            # update_user = await user_service.update_user(user_id=user_id, user=UpdateUser(gptResponse=gptResponse))
            print("result", result)
            print(data)
            return data
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating question: {e}")



    # async def create_question(self, request: Request, userquestion: UserQuestion):
    #     try:
    #         session_id = request.cookies.get("session_id")
    #         user_id = get_user_id_from_session(session_id)
    #         data = userquestion.dict()
            
    #         # gpt_response = self.ask_gpt(self, userquestion.question)
                      
    #         result = await self.repository.userquestion.create(data=data) #.gpt.create(data=data)
    #         print("result", result)
    #         return result
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Error creating question: {e}")