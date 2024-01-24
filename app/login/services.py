from app.settings.database import database
from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class LoginService:
    def __init__(self):
        self.repository = database
    
       