from fastapi import APIRouter, HTTPException, Depends
from app.payment.services import (
    CreatePayment,
    UpdatePayment,
    PaymentService,
)
from app.middlewares.jwt_handler import JWTBearer
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")

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


@router.post("/new", dependencies=[Depends(JWTBearer())])
async def create_payment(
    payment: CreatePayment, payment_service: PaymentService = Depends()
):
    try:
        new_payment = await payment_service.create_payment(payment)
        return new_payment

    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Fuck! Internal Server Error: {str(ex)}"
        )


@router.put("/{id}")
async def update_payment(
    id: int, payment: UpdatePayment, payment_service: PaymentService = Depends()
):
    return await payment_service.update_payment(payment_id=id, payment=payment)


@router.delete("/{id}")
async def delete_payment(id: int, payment_service: PaymentService = Depends()):
    return await payment_service.delete_payment(payment_id=id)


@router.post("/confirm",dependencies=[Depends(JWTBearer())])
async def stripe_payment_confirm(
    payment_intent_id: str, payment_service: PaymentService = Depends()
):
    """
    Stripe payment confirmation endpoint.
    
    Parameters:
        - payment_intent_id: str
        - payment_service: PaymentService
    
    Returns:
        The result of the payment confirmation.
    """
    payment_method = "pm_card_visa"
    result = await payment_service.stripe_payment_confirm(
        payment_intent_id, payment_method
    )
    if result is not None:
        status_code = 200
        stripe_payment_id = payment_intent_id
        return result
    else:
        raise HTTPException(status_code=400, detail=result)
