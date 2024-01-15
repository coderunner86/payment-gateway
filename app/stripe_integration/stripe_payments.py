import stripe

from pydantic import BaseModel
from pydantic import  ValidationError

import os
from dotenv import load_dotenv

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def get_payment_info():
    try:
        payments_info = stripe.PaymentIntent.list()

        return payments_info
    
    except Exception as e:
        return {"error": str(e)}
    


