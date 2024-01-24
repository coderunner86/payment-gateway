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
from app.helpers.session import create_session

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

"""
Route: POST /users/login

Description: Processes the login request and performs user authentication.
Successful response: RedirectResponse that redirects the user to the dashboard page.
Input parameters:
  - email: String representing the user's email.
  - password: String representing the user's password.
"""


@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = UserLogin(email=email, password=password)
    retrieve_user = await UserService().find_user_by_email(email=user.email)
    if not retrieve_user:
        raise HTTPException(status_code=401, detail="Invalid Email!")
    else:
        verified = Hasher.verify_password(
            plain_password=user.password, hashed_password=retrieve_user.password
        )
        if verified:
            uid = retrieve_user.id
            print("Welcome", retrieve_user.email)
            print("UID", retrieve_user.id)
            session_id = create_session(uid)

            token: str = create_token(user.dict())
            print("token:", token)
            print("session_id:", session_id)
            redirect_home = RedirectResponse(url="/login", status_code=303)

            response = RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie(
                key="session_id", value=session_id, httponly=True, secure=True
            )
            response.set_cookie(key="token", value=token, httponly=True, secure=True)
            return response if session_id != None else redirect_home

        else:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
