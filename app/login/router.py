from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.login.services import UserLogin
from app.auth.jwt_manager import create_token
from app.stripe_integration.stripe_users import get_customers_info

user_login = UserLogin

router = APIRouter(
    prefix="/home",
    tags=["home"],
)

@router.post('/login', tags=['auth'])
async def user_login(user: UserLogin):
    users_info = await get_customers_info()
    if not users_info:
        raise HTTPException(status_code=404, detail="Email not found")

    if user.email in [customer_info["email"] for customer_info in users_info.values()]:
        token: str  = create_token(user.dict()) 
        return JSONResponse(status_code=200, content=token)
    else:
        raise HTTPException(status_code=404, detail="Email not found")