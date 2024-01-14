import httpx
from fastapi import FastAPI, HTTPException
from fastapi_health import health

def get_all_routes(app: FastAPI):
    return [route.path for route in app.routes]

async def check_route_health(app: FastAPI):
    client = httpx.AsyncClient(app=app)
    all_routes = get_all_routes(app)
    responses = {}
    for route in all_routes:
        try:
            response = await client.get(route)
            responses[route] = response.status_code == 200
        except HTTPException as e:
            responses[route] = False
    await client.aclose()
    return responses