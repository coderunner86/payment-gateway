from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        Initialize the object with the given auto_error parameter.

        :param auto_error: a boolean indicating whether to automatically raise an error on failure
        :type auto_error: bool
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """
        Asynchronous method to validate HTTP authorization credentials.

        Args:
            request (Request): The HTTP request object.

        Returns:
            HTTPAuthorizationCredentials: The validated HTTP authorization credentials.

        Raises:
            HTTPException: If the credentials are invalid.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if self.validate_credentials(credentials.credentials):
                return credentials
            else:
                raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def validate_credentials(self, token: str) -> bool:
        """
        Validate the credentials using the provided token.

        Args:
            token (str): The token to be validated.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            # Lógica para validar el token
            data = validate_token(token)
            return data
        except Exception as e:
            return False
