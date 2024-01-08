from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional

from fastapi import HTTPException


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
        payment = await self.repository.payment.find_first(where={"id": payment_id})
        if not payment:
                raise HTTPException(status_code=404, detail="Payment ID not found")

        

        user = await self.repository.user.find_first(where={"id":payment.user_id})
        product = await self.repository.product.find_first(where={"id":payment.product_id})
        payment_info_by_id = {
                    "payment_id": payment.id,
                    "user_id": user.id if user else None,
                    "user_name": user.name if user else None,
                    "product_id": product.id if product else None,
                    "product_name": product.name if product else None,
                    "product_description": product.description if product else None, 
                    "amount": payment.amount,
                    "accepted": payment.accepted,
                    "created_at": payment.created_at.isoformat(),
                    "updated_at": payment.updated_at.isoformat(),
        }
            
        return payment_info_by_id
    
    
    async def find_all_payment(self):
        
        payments = await self.repository.payment.find_many()

        payment_history = []
        for payment in payments:
        
            user = await self.repository.user.find_first(where={"id": payment.user_id})
            product = await self.repository.product.find_first(where={"id": payment.product_id})

            payment_info = {
                "payment_id": payment.id,
                "user_id": user.id if user else None,
                "user_name": user.name if user else None,
                "product_id": product.id if product else None,
                "product_name": product.name if product else None,
                "product_description": product.description if product else None, 
                "amount": payment.amount,
                "accepted": payment.accepted,
                "created_at": payment.created_at.isoformat(),
                "updated_at": payment.updated_at.isoformat(),
            }
            payment_history.append(payment_info)

        return payment_history


    async def create_payment(self, payment: CreatePayment):
    
            user_exists = await self.repository.user.find_first(where={"id": payment.user_id})
            if not user_exists:
                return {"error": "User not found"}

            product_exists = await self.repository.product.find_first(where={"id": payment.product_id})
            if not product_exists:
                return {"error": "Product not found"}

            new_payment = await self.repository.payment.create(data = payment.dict())
            paymetnt_info = {
                "payment id": new_payment.id,
                "user id": user_exists.id,
                "user name": user_exists.name,
                "product id": product_exists.id,
                "product": product_exists.name,
                "product description": product_exists.description, 
                "amount": new_payment.amount,
                "accepted": new_payment.accepted,
                "created_at": new_payment.created_at.isoformat(),
                "updated_at": new_payment.updated_at.isoformat(),
                }    
            return {"message": "payment created succesfully", "payment info": paymetnt_info}, 201


    async def update_payment(self, payment_id: int, payment: UpdatePayment):

                payment_exists = await self.repository.payment.find_first(where={"id": payment_id})
                
                if not payment_exists:
                    raise HTTPException(status_code=404, detail="Payment ID not found")

                updated_payment = await self.repository.payment.update(
                    where={"id": payment_id},
                    data=payment.dict(),
                
                )
                
                product = await self.repository.product.find_first(where={"id": payment.product_id})
                if not product:
                    return {"error": "Product not found"}
                
                product = await self.repository.product.find_first(where={"id": updated_payment.product_id})
                if product:
                    payment_info = {
                        "id": updated_payment.id,
                        "amount": updated_payment.amount,
                        "accepted": updated_payment.accepted,
                        "created_at": updated_payment.created_at.isoformat(),
                        "updated_at": updated_payment.updated_at.isoformat(),
                    }
                    payment_info["product"] = product.name
    
                return {
                    "message": f'Payment {payment_id} updated successfully',
                    "payment": payment_info
                }
                    
        
    async def delete_payment(self, payment_id: int):
        payment_exists = await self.repository.payment.find_first(where={"id": payment_id})
        if not payment_exists:
            raise HTTPException(status_code=404, detail="Payment ID not found")        

        await self.repository.payment.delete(where={"id": payment_id})
        return  {"message": f"Payment {payment_id} deleted successfully"}, 200
