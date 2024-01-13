from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if self.validate_credentials(credentials.credentials):
                return credentials
            else:
                raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def validate_credentials(self, token: str) -> bool:
        try:
            # Lógica para validar el token
            data = validate_token(token)
            return data
        except Exception as e:
            return False
