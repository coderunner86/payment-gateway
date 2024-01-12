from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

#stripe imports
from app.stripe_integration.stripe_users import get_customers_info
from app.middlewares.jwt_handler import JWTBearer
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/customers", response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def customers_dashboard(request: Request):
    users = await get_customers_info()
    return templates.TemplateResponse("dashboard.html", context={"request": request, "users": users})