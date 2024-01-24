from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
class ErrorHamdler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try: 
            return await call_next(request)
        except HTTPException as exc:
            if exc.status_code == 401:
                return templates.TemplateResponse("login.html", {"request": request, "alert": exc.detail})
        except Exception as ex:
            return JSONResponse(status_code=500, content={'error':str(ex)})
    