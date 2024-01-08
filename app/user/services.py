from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional

class CreateUser(BaseModel):
    id: int
    name:str 
    last_name: Optional[str] = None


class UpdateUser(BaseModel):
    name: str
    last_name: str

class UserService:
    def __init__(self):
        self.repository = database

    async def find_user(self, user_id: int):
        result = await self.repository.user.find_first(where={"id": user_id})
        return result

    async def find_all_user(self):
        result = await self.repository.user.find_many(
        )

        return result
    async def create_user(self, user: CreateUser):
        try:
            new_user = await self.repository.user.create(data=user.dict())
            return {"message": "User created successfully", "user": new_user}
        except Exception as ex:
            return {"error": str(ex)}


    async def update_user(self, user_id: int, user: UpdateUser):
        try:
            result = await self.repository.user.update(
                where={"id": user_id},
                data=user.dict(),
             
            )
            return {"message": f'User {user_id} updated successfully', "result": result}
        except Exception as ex:
            return {"error": str(ex)}
        
    async def delete_user(self, user_id: int):
        result = await self.repository.user.delete(where={"id": user_id})
        return result
