import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from settings.routers import register_router
from app.middlewares.check_routes import check_route_health  # Asegúrate de importar correctamente tu función

@pytest.mark.asyncio
async def test_check_route_health():
    app = FastAPI()

    # Aquí configuras tu aplicación, por ejemplo, agregando rutas
    app.include_router(register_router)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        health_check_results = await check_route_health(app)
    
    for route, is_healthy in health_check_results.items():
        assert is_healthy, f"La ruta {route} falló en el health check"
