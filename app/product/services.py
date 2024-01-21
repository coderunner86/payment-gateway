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
        try:
            # print(product_id)  
            archived_product = stripe.Product.modify(product_id, active=False)
            prices = stripe.Price.list(product=product_id)
            # print(prices)
            for price in prices.auto_paging_iter():
                stripe.Price.modify(price.id, active=False)
            print(archived_product)
            return archived_product
        except stripe.error.StripeError as ex:
            return {"error on the service": str(ex)}
