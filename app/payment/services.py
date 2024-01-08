from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional


class PaymentBase(BaseModel):
    amount: float
    accepted: Optional[bool] = False

class CreatePayment(PaymentBase):
    user_id: int
    product_id: int

class UpdatePayment(BaseModel):
    product_id: int
    amount: float

class Payment(PaymentBase):
    id: int
    user_id: int
    payment_id: int
    amount: float

class PaymentService:
    def __init__(self):
        self.repository = database

    async def find_payment(self, payment_id: int):
        result = await self.repository.payment.find_first(where={"id": payment_id})
        return result
    
    
    async def find_all_payment(self):
        result = await self.repository.payment.find_many(
        )

        return result


    async def create_payment(self, payment: CreatePayment):
        try:    
            user_exists = await self.repository.user.find_first(where={"id": payment.user_id})
            if not user_exists:
                return {"error": "User not found"}

            product_exists = await self.repository.product.find_first(where={"id": payment.product_id})
            if not product_exists:
                return {"error": "Product not found"}

            new_payment = await self.repository.payment.create(data = payment.dict())
            return {"message": "payment created succesfully", "user":new_payment}
        except Exception as ex:
            return {"error": str(ex)}

    async def update_payment(self, payment_id: int, payment: UpdatePayment):
            try:
                product = await self.repository.product.find_first(where={"id": payment.product_id})
                if not product:
                    return {"error": "Product not found"}
                result = await self.repository.payment.update(
                    where={"id": payment_id},
                    data=payment.dict(),
                
                )
                return {"message": f'payment {payment_id} updated successfully', "result": result}
            except Exception as ex:
                return {"error": str(ex)}
            
        
    async def delete_payment(self, payment_id: int):
        result = await self.repository.payment.delete(where={"id": payment_id})
        return result
