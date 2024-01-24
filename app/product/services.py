from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional
import stripe
class CreateProduct(BaseModel):
    id: int
    name:str
    description:Optional[str] = None
    price:float

class UpdateProduct(BaseModel):
    name: str
    description: str
    price:float

class ProductService:
    def __init__(self):
        self.repository = database

    async def find_product(self, product_id: int):
        result = await self.repository.product.find_first(where={"id": product_id})
        return result
    
    
    async def find_all_product(self):
        result = await self.repository.product.find_many(
        )

        return result


    async def create_product(self, product: CreateProduct):
        """
        Asynchronously creates a new product using the provided CreateProduct instance.

        Args:
            self: The class instance.
            product: An instance of CreateProduct.

        Returns:
            A dictionary containing a success message and the created product id, 
            or an error message in case of an exception.
        """
        try:    
            new_product = await self.repository.product.create(data = product.dict())
            new_stripe_product = stripe.Product.create(name=new_product.name, description=new_product.description)
            new_product = new_product.dict()
            new_product["stripeProductId"] = new_stripe_product["id"]
            stripeProductId = new_product["stripeProductId"]
            await self.repository.product.update(where={"id": new_product["id"]}, data={"stripeProductId": stripeProductId})
            new_product_price = stripe.Price.create(
                unit_amount=new_product["price"]*100, currency="usd", product_data={"name": new_product["name"]},
            )
            return {"message": "Product created succesfully", "product id":new_product["stripeProductId"]}
        except Exception as ex:
            return {"error": str(ex)}

    async def update_product(self, product_id: int, product: UpdateProduct):
            try:
                result = await self.repository.product.update(
                    where={"id": product_id},
                    data=product.dict(),
                
                )
                return {"message": f'Product {product_id} updated successfully', "result": result}
            except Exception as ex:
                return {"error": str(ex)}
            
        
    async def delete_product(self, product_id: int):
        result = await self.repository.product.delete(where={"id": product_id})
        return result
    
    def archive_by_prod_id(self, product_id: str):
        """
        Archive a product by its ID and deactivate associated prices. 

        Args:
            product_id (str): The ID of the product to be archived.

        Returns:
            dict: The archived product details, or an error message if the operation fails.
        """
        try:
            archived_product = stripe.Product.modify(product_id, active=False)
            prices = stripe.Price.list(product=product_id)
            for price in prices.auto_paging_iter():
                stripe.Price.modify(price.id, active=False)
            # print(archived_product)
            return archived_product
        except stripe.error.StripeError as ex:
            return {"error on the service": str(ex)}
        
    def unarchive_by_prod_id(self, product_id: str):
        try:
            unarchived_product = stripe.Product.modify(product_id, active=True)
            # print(unarchived_product)
            return unarchived_product
        except stripe.error.StripeError as ex:
            return {"error on the service": str(ex)}
        
    def get_stripe_product():
        """
        Retrieves a list of active Stripe products and returns a dictionary containing their IDs, names, descriptions, and images.

        Returns:
            product_dict (dict): A dictionary containing the following keys:
                - ids (list): A list of product IDs.
                - names (list): A list of product names.
                - descriptions (list): A list of product descriptions.
                - images (list): A list of product images.

        Raises:
            stripe.error.StripeError: If an error occurs while retrieving the Stripe products.
        """
        try:
            products = stripe.Product.list(active=True)
            ids = [product.id for product in products]
            names = [product.name for product in products]
            descriptions = [product.description for product in products]
            images = [product.images for product in products]

            product_dict = {"ids": ids, "names": names, "descriptions": descriptions, "images": images}
             
            return product_dict
        except stripe.error.StripeError as ex:
            return {"error on the get_stripe_product service": str(ex)}
