
from fastapi import APIRouter, Request, Form
from fastapi import HTTPException

from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.responses import Response

from app.auth.jwt_manager import create_token
from app.stripe_integration.stripe_users import get_customers_info
from app.login.services import UserLogin
from app.user.services import UserService
from app.settings.database import database

from app.auth.hashing import Hasher
import uuid
templates = Jinja2Templates(directory="app/templates")
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

"""
Route: GET /users/login

Description: Renders the login form in HTML.
Successful response: HTMLResponse with the content of the login form.
Input parameters:
  - request: Request object of type Request from FastAPI used to receive the HTTP request.
"""
@router.get('/login', response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


"""
Route: POST /users/login

Description: Processes the login request and performs user authentication.
Successful response: RedirectResponse that redirects the user to the dashboard page.
Input parameters:
  - email: String representing the user's email.
  - password: String representing the user's password.
"""    
@router.post('/login')
async def login(email: str = Form(...), password: str = Form(...)):
    user = UserLogin(email=email, password=password)
    retrieve_user = await UserService().find_user_by_email(email=user.email)
    if not retrieve_user:
        found = False #to check if email exists in the database or not, if not then raise an exception to break
        raise HTTPException(status_code=400, detail="Email not found")
    else:
        verified = Hasher.verify_password(plain_password=user.password, hashed_password=retrieve_user.password)
        print(verified)
        found = True
        if found and verified:
            print('Welcome',retrieve_user.email)
            print('UID',retrieve_user.id)
            session_id = str(uuid.uuid4())
            session_id=session_id.replace('-', '')
            token: str = create_token(user.dict())
            print("token:", token)
            print("session_id:", session_id)
            response = Response('/users/dashboard')
            response.set_cookie(key="session_id", value=token, httponly=True, secure=True)
            redirect_response = RedirectResponse(url='/api/users/dashboard', status_code=303)
            # session_id = None
            redirect_response.set_cookie(key="token", value=token, httponly=True, secure=True)
            return redirect_response if session_id != None else token  
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        