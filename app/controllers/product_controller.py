from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# stripe imports
from app.stripe_integration.stripe_products import get_payment_links
from app.middlewares.jwt_handler import JWTBearer

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/products", tags=["products"])


# 
@router.get("/catalog", response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
async def payment_links(request: Request):
    products_links = await get_payment_links()
    return templates.TemplateResponse(
        "catalog.html", context={"request": request, "products_links": products_links}
    )
