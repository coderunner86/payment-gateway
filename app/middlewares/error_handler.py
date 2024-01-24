from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
class ErrorHamdler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        """
        Initializes the class with the provided FastAPI app.

        Args:
            app (FastAPI): The FastAPI app to initialize with.

        Returns:
            None
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        """
        Asynchronously dispatches the request to the next callable and handles exceptions.

        Args:
            self: The instance of the class.
            request (Request): The incoming request.
            call_next (Callable): The next callable to be called.

        Returns:
            Response | JSONResponse: The response from the callable or an error response.
        """
        try: 
            return await call_next(request)
        
        except HTTPException as exc:
            
            if exc.status_code == 401:
                return templates.TemplateResponse("login.html", {"request": request, "alert": exc.detail})
        
        except Exception as ex:
        
            return JSONResponse(status_code=500, content={'error':str(ex)})
    