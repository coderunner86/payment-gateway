import stripe

from pydantic import BaseModel
from pydantic import  ValidationError

import os
from dotenv import load_dotenv

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


async def get_customers_info():
            try:
                customers = stripe.Customer.list(limit=10) 
                customers_info = []
                customers_info = {cus.id: {"name": cus.name, "email": cus.email} for cus in customers.data}

                return customers_info
            
            except Exception as e:
                return {"error": str(e)}
        
