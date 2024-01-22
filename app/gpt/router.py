
from fastapi import APIRouter, HTTPException, Request
from app.gpt.services import GptService, UserQuestion
from app.helpers.session import get_user_id_from_session
import os
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("API_KEY")
gpt_service = GptService(API_KEY)

router = APIRouter( prefix="/gpt", tags=["gpt"])

@router.post("/ask-gpt")
async def ask_gpt_endpoint(request: Request, user_question: UserQuestion):
    try:
        result = await gpt_service.create_question(request, user_question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


