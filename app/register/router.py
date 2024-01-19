from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.auth.jwt_manager import create_token
from app.helpers.session import create_session

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
            print("the user we will create", user)
            retrieve_user = await UserService().find_user_by_email(email=user.email)
            if retrieve_user == None:
                users_id = await UserService().find_all_user()
                if not users_id:
                    first_user = await UserService().create_user(user) 
                else:
                    last_user_id = users_id[-1].id
                    uid = last_user_id + 1
                    session_id = create_session(uid)
                    token: str = create_token(user.dict())
                    response = RedirectResponse(url="/dashboard", status_code=303)
                    response.set_cookie(
                    key="session_id", value=session_id, httponly=True, secure=True
                )
                    response.set_cookie(key="token", value=token, httponly=True, secure=True)
                    
                    try: 
                        result = await UserService().create_user(user)
                        print("This is the result when we create a user", result)
                        return  response
                    except Exception as ex:
                        return(f'{"This error is when we try to create the user": str(ex)}')
                        
            elif retrieve_user.email == user.email:
                print("retrieve_user",retrieve_user.email)
                exist = retrieve_user.email
                print(exist)
                print("Email already exists!")
                return {"error": "Email already exists!"} 