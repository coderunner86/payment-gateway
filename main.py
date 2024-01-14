import os
import stripe
import uvicorn

from fastapi import FastAPI, Depends
from fastapi_health import health

from dotenv import load_dotenv

from app.settings.database import database
from app.settings.environment import settings
from app.settings.routers import routers

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.middlewares.error_handler import ErrorHamdler
from app.middlewares.check_routes import check_route_health
env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)


def get_session():
    return True


def healthy_condition():
    return {"database": "online"}


def sick_condition():
    return False

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(ErrorHamdler)

templates = Jinja2Templates(directory="app/templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def health_check_wrapper():
    return await check_route_health(app)

@app.on_event("startup")
async def startup():
    await database.connect()
    [app.include_router(router, prefix=prefix) for router in routers]
    app.add_api_route("/health", health([health_check_wrapper]))


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

prefix = "/api"
[app.include_router(router, prefix=prefix) for router in routers]

if __name__ == "__main__":
    port = settings.get("app").get("port")
    uvicorn.run(app, host="0.0.0.0", port=port)