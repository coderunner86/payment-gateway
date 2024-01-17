import os
import stripe
import uvicorn

from fastapi import FastAPI, Request, Depends, Response, HTTPException


from dotenv import load_dotenv

from app.settings.database import database
from app.settings.environment import settings
from app.settings.routers import routers
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates


from app.middlewares.error_handler import ErrorHamdler
from app.middlewares.jwt_handler import JWTBearer

#stripe imports
from app.stripe_integration.stripe_users import get_customers_info
from app.stripe_integration.stripe_products import get_payment_links
from app.stripe_integration.stripe_payments import get_payment_info
env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(ErrorHamdler)

templates = Jinja2Templates(directory="app/templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/dashboard", response_class=HTMLResponse)
async def customers_dashboard(request: Request):
    session_id = request.cookies.get("session_id")
    token = request.cookies.get("token")
    if not token or not session_id:
        return RedirectResponse(url='/login', status_code=303)
    users = await get_customers_info()
    return templates.TemplateResponse("dashboard.html", context={"request": request, "users": users})

@app.get("/thankyou", response_class=HTMLResponse)
async def customers_dashboard(request: Request):
    token = request.cookies.get("token")
    session_id = request.cookies.get("session_id")
    if not token or not session_id:
        return RedirectResponse(url='/login', status_code=303)
    return templates.TemplateResponse("thankyou.html", context={"request": request})

@app.get('/login', response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/catalog", response_class=HTMLResponse)
async def payment_links(request: Request):
    token = request.cookies.get("token")
    session_id = request.cookies.get("session_id")
    if not token or not session_id:
        return RedirectResponse(url='/login', status_code=303)
    products_links = await get_payment_links()
    return templates.TemplateResponse(
        "catalog.html", context={"request": request, "products_links": products_links}
    )


@app.get("/payments", response_class=HTMLResponse)
async def payment_info(request: Request):
    session_id = request.cookies.get("session_id")
    token = request.cookies.get("token")
    if not token or not session_id:
        return RedirectResponse(url='/login', status_code=303)
    products = await get_payment_info()
    return templates.TemplateResponse(
        "payments.html", context={"request": request, "products": products}
    )

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url='/login', status_code=303)
    response.delete_cookie("token")
    response.delete_cookie("session_id")
    return response



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


prefix = "/api"
[app.include_router(router, prefix=prefix) for router in routers]

if __name__ == "__main__":
    port = settings.get("app").get("port")
    uvicorn.run(app, host="0.0.0.0", port=port)