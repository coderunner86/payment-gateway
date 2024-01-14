from app.settings.database import database
from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class RegisterService:
    def __init__(self):
        self.repository = database