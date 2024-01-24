import os
from dotenv import load_dotenv
import stripe 

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def get_payment_links():
        """
        Asynchronously retrieves payment links and related product information from the Stripe API.
        Returns a list of tuples containing the payment links, product names, product images, and descriptions.
        If an exception occurs, returns a dictionary with the error message.
        """
        try:
        
            links = [link.url for link in stripe.PaymentLink.list(limit=100, active=True).data]
            productos = [producto.name for producto in stripe.Product.list(limit=100).data]        


            linarray = [i for i in range(1, len(links)+1)]
            shift_linarray = [i-1 for i in linarray]

            productos_invertidos = list.reverse(productos)
            shift_productos = [productos[i-1] for i in shift_linarray]
            productos_invertidos = shift_productos[::1]
            
            images = [product.images for product in stripe.Product.list(limit=100).data]
            images_invertidos = list.reverse(images)  
            shift_images = [images[i-1] for i in shift_linarray]
            images_invertidos = shift_images[::1]    
            
            desc = [product.description for product in stripe.Product.list(limit=100).data]  
            desc_invertidos = list.reverse(desc)
            shift_desc = [desc[i-2] for i in shift_linarray]
            desc_invertidos = shift_desc[::1]                

            links_y_productos = [(link, nombre, imagen, desc) for link, nombre, imagen, desc in zip(links, productos_invertidos, images_invertidos, desc_invertidos)]
            
            return links_y_productos

        except Exception as e:
            return {"error": str(e)}

