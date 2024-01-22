
from fastapi import APIRouter, HTTPException
from app.gpt.services import GptService
import os
from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv("API_KEY")
gpt_service = GptService(API_KEY)

router = APIRouter( prefix="/gpt", tags=["gpt"])

@router.post("/ask-gpt")
def ask_gpt(question: str):
    try:
        response = gpt_service.ask_gpt(question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

