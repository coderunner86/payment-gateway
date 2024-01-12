from fastapi import Request, HTTPException
from fastapi.security.http import HTTPBearer
from app.auth.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@email.com":
            raise HTTPException(status_code=403, detail="Bad credentials")
