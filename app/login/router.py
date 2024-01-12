from fastapi import APIRouter, Request, Form
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.responses import Response

from app.auth.jwt_manager import create_token
from app.stripe_integration.stripe_users import get_customers_info
from app.login.services import UserLogin

user_login = UserLogin
templates = Jinja2Templates(directory="app/templates")
router = APIRouter(
    prefix="/home",
    tags=["home"],
)

@router.get('/login', response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

    
@router.post('/login')
async def process_login_form(email: str = Form(...), password: str = Form(...)):
    user = UserLogin(email=email, password=password)
    users_info = await get_customers_info()
    print('users_info', users_info)
    if not users_info:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if user.email in [customer_info["email"] for customer_info in users_info.values()]:
        token: str = create_token(user.dict())
        # return {"token": token}
        response = Response('/login')
        response.set_cookie(key="token", value=token, httponly=True, secure=True)
        return RedirectResponse(url='/api/users/customers', status_code=303) 
    else:
        raise HTTPException(status_code=404, detail="Email not found")