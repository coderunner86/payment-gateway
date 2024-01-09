from fastapi import APIRouter, HTTPException, Depends

from app.payment.services import CreatePayment, UpdatePayment, PaymentService, ConfirmPayment

import requests

payment_service = PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.get("/{id:int}")
async def get_payment(id: int, payment_service: PaymentService = Depends()):
    return await payment_service.find_payment(payment_id=id)

@router.get("")
async def get_all_payments(payment_service: PaymentService = Depends()):
    return await payment_service.find_all_payment()

@router.post("/")
async def create_payment(payment: CreatePayment, payment_service: PaymentService= Depends()):
    try:
        new_payment = await payment_service.create_payment(payment)
        return new_payment
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fuck! Internal Server Error: {str(ex)}")


@router.post("/confirm")
async def stripe_payment_confirm(payment_intent_id: str, payment_service: PaymentService = Depends()):
    payment_method = 'pm_card_visa'
    result = await payment_service.stripe_payment_confirm(payment_intent_id, payment_method)
    status_code = 200
    if status_code != 200:
        raise HTTPException(status_code=400, detail=result)
    return result
    
    # pass


@router.put("/{id}")
async def update_payment(id: int, payment: UpdatePayment, payment_service:PaymentService = Depends()):
    return await payment_service.update_payment(payment_id=id, payment=payment)


@router.delete("/{id}")
async def delete_payment(id: int, payment_service: PaymentService = Depends()):
    return await payment_service.delete_payment(payment_id=id)
