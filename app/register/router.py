from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.responses import Response

from app.auth.jwt_manager import create_token
from app.user.services import UserService
from app.register.services import UserRegister

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users", tags=["users"],
)

    
@router.get('/register', response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
    ):
        
            user = UserRegister(name=name, email = email, password = password)
            print(user)
            retrieve_user = await UserService().find_user_by_email(email=user.email)
            if retrieve_user == None:
                token: str = create_token(user.dict())
                response = Response('/register')
                response.set_cookie(key="token", value=token, httponly=True, secure=True)
                try: 
                    result = await UserService().create_user(user)
                    return  result
                except Exception as ex:
                    return {"error": str(ex)}
            elif retrieve_user.email == user.email:
                print("retrieve_user",retrieve_user.email)
                exist = retrieve_user.email
                print(exist)
                print("Email already exists!")
                return {"error": "Email already exists!"} 
