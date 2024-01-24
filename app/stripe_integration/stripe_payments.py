import os
from dotenv import load_dotenv
import stripe

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

### List Payments ###
async def get_payment_info():
    try:
        payments_info = stripe.PaymentIntent.list()
        return payments_info
    except Exception as e:
        return {"error": str(e)}
