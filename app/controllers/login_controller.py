from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/home",
    tags=["home"]
)

@router.get("/userlogin", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
