from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional

from fastapi import HTTPException
import stripe
import os
from dotenv import load_dotenv

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class PaymentBase(BaseModel):
    amount: int
    accepted: Optional[bool] = False

class CreatePayment(PaymentBase):
    user_id: int
    product_id: int

class UpdatePayment(BaseModel):
    product_id: int
    amount: int
    stripe_payment_id: str  
    status: str   
    payment_method_types: str

class Payment(PaymentBase):
    id: int
    user_id: int
    payment_id: int
    amount: int
    stripe_payment_id: str  
    status: str   
    payment_method_types: str

class AbstractModel(PaymentBase):
    payment_method: str
    
class ConfirmPayment(AbstractModel):
    product_id: int
    

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

    #This method will create a payment intent
    async def create_payment(self, payment: CreatePayment):
    
            user_exists = await self.repository.user.find_first(where={"id": payment.user_id})
            if not user_exists:
                return {"error": "User not found"}

            product_exists = await self.repository.product.find_first(where={"id": payment.product_id})
            if not product_exists:
                return {"error": "Product not found"}
            
            new_payment = await self.repository.payment.create(data = payment.dict())

            payment_info = {
                "payment id": new_payment.id,
                "user id": user_exists.id,
                "user name": user_exists.name,
                "product id": product_exists.id,
                "product": product_exists.name,
                "product description": product_exists.description, 
                "amount": new_payment.amount,
                "created_at": new_payment.created_at.isoformat(),
                "updated_at": new_payment.updated_at.isoformat(),
                }
          
            payment_id = payment_info["payment id"]
            amount = payment_info["amount"]
            confirm_payment_url = 'localhost:8000/confirm'
            try:
                payment_intent = await self.stripe_payment_intent(new_payment.id)
                print('*********************')
                print(type(payment_intent))
                if payment_intent.get("Success"):
                    new_payment.accepted = True
                    charge = payment_intent["charge"]
                    payment_intent_id = payment_intent["payment_intent_id"]
                    payment_method = payment_intent["payment_method"]
                    payment_status = payment_intent["status"]
                    await self.repository.payment.update(data = {"accepted": True, "stripe_payment_id": payment_intent_id, "payment_method_types": payment_method, "status": payment_status }, where={"id": new_payment.id})
                    return {"message": "Payment created successfully", "payment_info": payment_info, "charge": charge,"payment_intent_id":payment_intent_id, "payment_method_types": payment_method, "status": payment_status, "redirect url": confirm_payment_url}, 201
                
                else:
                    return {"error": "Payment processing failed", "details": payment_intent.get("error")}, 400
            
            except HTTPException as http_exc:
                print(f"Se ha producido una excepción HTTP: {http_exc.detail}")
                raise HTTPException(status_code=http_exc.status_code, detail=http_exc.detail)
            
            except Exception as ex:
                return {"error": str(ex)}, 500


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

    
#--------------------------------------------------
#          PAYMENT PROCESSING METHODS             #                        
#           (Stripe API v1 integration)           #
#--------------------------------------------------
            

### Create Payment Intent ###
    
    #This method will process the payment intent by charge the debit or credit card of the user
    async def stripe_payment_intent(self, payment_id: int):
        payment = await self.find_payment(payment_id)
        amount = payment["amount"]    
        if not payment:
            return {"error": "Payment intent not found"}
        try:
            charge = "ch_1NirD82eZvKYlo2CIvbtLWuY" #foo value
            result = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            automatic_payment_methods={"enabled": True}, #obtained from Stripe dashboard
            description=charge        
            )
            return {"Success": True, "charge": charge, "payment_intent_id": result.id, "payment_method": result.payment_method, "status":result.status }
        except stripe.errro.StripeError as e:
            
            return {"error": str(e)}
        
 ### Get Payment Links ###       

    async def get_payment_links():
        try:
            payment_links = stripe.PaymentLink.list(limit=100, active=True)
            productos = stripe.Product.list(limit=100).data 

            links_y_productos = {}
            productos_invertidos = productos[::-1]
            
            for index, link in enumerate(payment_links.data):
                producto = productos_invertidos[index]
                links_y_productos[link.url] = producto.name
            return links_y_productos

        except Exception as e:
            return {"error": str(e)}
    
### Confirm Payment method ###
    async def find_stripe_payment(self, stripe_payment_id: str):
        strpe_payment_info_by_id = await self.repository.payment.find_first(where={"stripe_payment_id": stripe_payment_id})
        if not strpe_payment_info_by_id:
                raise HTTPException(status_code=404, detail="Payment ID not found")
        return strpe_payment_info_by_id

    async def stripe_payment_confirm(self, payment_intent_id: str, payment_method: str):
        try:      
            result = stripe.PaymentIntent.confirm(payment_intent_id, payment_method=payment_method, return_url="https://www.example.com",), 

            # Desempaquetar y obtener los valores JSON
            *other, jsonvals = result
            jsonvals = dict(jsonvals)
            print('-----------------------------')
            print(type(jsonvals))
            print(f"result stripe_payment_confirm: {jsonvals}")
             # Consultar la información de pago
            stripe_payment_info = await self.find_stripe_payment(payment_intent_id)
            print("_________________________________________")
            print(f"stripe_payment_info query: {stripe_payment_info}")
            stripe_payment_method = jsonvals['payment_method_types']
            payment_status = jsonvals['status']
            print(f"stripe_payment_id {stripe_payment_info.stripe_payment_id}")
            stripe_payment_info.stripe_payment_id = 'opera'
            print(f"stripe_payment_info_: {stripe_payment_info}")
            print("_________________________________________")
            print(f"stripe payment method: {stripe_payment_method}")
            print(f"payment status: {payment_status}")
            print("_________________________________________")
            # Actualizar el diccionario con los nuevos valores
            stripe_payment_info.payment_method_types = 'Fisico'
            a = stripe_payment_info.payment_method_types
    
            # a = ', '.join(a)
            print(f"stripe_payment_info after: {a}")
            print(f"stripe payment method: {stripe_payment_method}")
            print(f"payment status: {payment_status}")
            b = ', '.join(stripe_payment_method)
            c = payment_status
            # Actualizar en base de datos (descomenta la siguiente línea si es necesario)
            await self.repository.payment.update(data = 
                                                 {"payment_method_types": b, "status": payment_status}, 
                                                  where={"id": stripe_payment_info.id })
            return result
        except Exception as ex:
            return {"message": f"An error has ocurred {ex}"}

