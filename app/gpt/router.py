from fastapi import APIRouter, HTTPException, Request
from app.gpt.services import GptService, UserQuestion
from fastapi import APIRouter, HTTPException, Request
from app.gpt.services import GptService, UserQuestion

router = APIRouter(prefix="/gpt", tags=["gpt"])
gpt_service = GptService()


@router.post("/ask-gpt")
async def ask_gpt_endpoint(request: Request, user_question: UserQuestion):
    """
    An asynchronous function for handling the 'ask-gpt' endpoint POST request. 
    Takes a Request object and a UserQuestion object as parameters. 
    Returns the result of creating a question using the GPT service. 
    If an exception occurs, it raises an HTTPException with status code 500 
    and the exception details as a string.
    """
    try:
        result = await gpt_service.create_question(request, user_question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
