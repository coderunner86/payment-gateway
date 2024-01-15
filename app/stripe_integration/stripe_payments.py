import stripe

from pydantic import BaseModel
from pydantic import  ValidationError

import os
from dotenv import load_dotenv

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
    
  
### List Payment Links ###       
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
 