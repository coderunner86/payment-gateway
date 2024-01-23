from fastapi import APIRouter, HTTPException, Request
from app.gpt.services import GptService, UserQuestion
from fastapi import APIRouter, HTTPException, Request
from app.gpt.services import GptService, UserQuestion

router = APIRouter(prefix="/gpt", tags=["gpt"])
gpt_service = GptService()

@router.post("/ask-gpt")
async def ask_gpt_endpoint(request: Request, user_question: UserQuestion):
    try:
        result = await gpt_service.create_question(request, user_question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))