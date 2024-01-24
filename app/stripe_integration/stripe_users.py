import os
from dotenv import load_dotenv
import stripe

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def get_customers_info():
            """
            Asynchronously retrieves information about customers.

            Returns:
                dict: A dictionary containing customer information, or an error dictionary if an exception is encountered.
            """
            try:
                customers = stripe.Customer.list(limit=10) 
                customers_info = []
                customers_info = {cus.id: {"name": cus.name, "email": cus.email} for cus in customers.data}

                return customers_info
            
            except Exception as e:
                return {"error": str(e)}
def delete_stripe_customer(customer_id):
    try:
        deleted_customer = stripe.Customer.delete(customer_id)
        return deleted_customer
    except stripe.error.StripeError as e:
        raise e
