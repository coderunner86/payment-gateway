from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

#stripe imports
from app.stripe_integration.stripe_users import get_customers_info
from app.middlewares.jwt_handler import JWTBearer
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
Bearer = JWTBearer()
print("Bearer",Bearer)
# 
@router.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def customers_dashboard(request: Request):
    token = request.cookies.get("token")
    print("received token",token)
    if not token:
        return RedirectResponse(url='/api/users/login', status_code=303)
    users = await get_customers_info()
    return templates.TemplateResponse("dashboard.html", context={"request": request, "users": users})


@router.get("/thankyou", response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def customers_dashboard(request: Request):
    token = request.cookies.get("token")
    print("received token",token)
    if not token:
        return RedirectResponse(url='/api/users/login', status_code=303)
    users = await get_customers_info()
    return templates.TemplateResponse("thankyou.html", context={"request": request, "users": users})
