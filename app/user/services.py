from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional
from app.auth.hashing import Hasher

import stripe

class CreateUser(BaseModel):
    id: int
    name:str 
    last_name: Optional[str] = None
    email: str
    password: str

class CreateStripeUser(BaseModel):
    id: int
    cus_id:str 
    user_id: str

class UpdateUser(BaseModel):
    name: str
    last_name: str

class UserService:
    def __init__(self):
        self.repository = database

    async def find_user(self, user_id: int):
        result = await self.repository.user.find_first(where={"id": user_id})
        return result
    async def find_user_by_email(self,  email: str):
        result = await self.repository.user.find_first(where={"email": email})
        return result
    async def find_all_user(self):
        result = await self.repository.user.find_many(
        )

        return result
    async def create_user(self, user: CreateUser, stripe_user=CreateStripeUser):
        try:
            encripted_password = Hasher.get_password_hash(user.password)
            user_data = user.dict()
            user_data['password'] = encripted_password

            new_user = await self.repository.user.create(data=user_data)
            stripe_user = stripe.Customer.create(
            email=new_user.email,
            name=new_user.name
        )   
            stripe_data = {"cus_id": stripe_user["id"], "user_id": new_user.id}
            new_stripe_user = await self.repository.stripeuser.create(
               data = stripe_data 
            )
            return  {"message": "User created successfully", "user": {"stripe_id": stripe_user["id"]}}
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
    

# StripeUser Handler service
# TODO: 
# Review the logic of this service, it's not clean and it should be refactored
    # Check if the logic increment future workload for the database
# Check if the user already exist in Stripe
# Check if the user already exist in the database
     
    async def create_stripe_user(self, user: CreateStripeUser):
        try:
            new_user = await self.repository.user.create(data = user.dict())
            return  {"message": "User created successfully"}
        except Exception as ex:
            return {"error": str(ex)}
    async def update_stripe_user(self, user_id: int, user: CreateStripeUser):
        try:
            result = await self.repository.user.update(
                where={"id": user_id},
                data=user.dict(),
             
            )
            return {"message": f'User {user_id} updated successfully', "result": result}
        except Exception as ex:
            return {"error": str(ex)}
        