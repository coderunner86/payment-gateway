import stripe

from pydantic import BaseModel
from pydantic import  ValidationError

import os
from dotenv import load_dotenv

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


import stripe

async def get_payment_links():
        try:
        
            links = [link.url for link in stripe.PaymentLink.list(limit=100, active=True).data]
            productos = [producto.name for producto in stripe.Product.list(limit=100).data]        

            productos_invertidos = list.reverse(productos)

            linarray = [i for i in range(1, len(links)+1)]
            shift_linarray = [i-1 for i in linarray]
            
            shift_productos = [productos[i-2] for i in shift_linarray]
            productos_invertidos = shift_productos[::1]
            
            links_y_productos = dict(zip(links, productos_invertidos))
            
            return links_y_productos, productos

        except Exception as e:
            return {"error": str(e)}

