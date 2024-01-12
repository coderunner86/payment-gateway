from app.settings.database import database
from pydantic import BaseModel
from pydantic import  ValidationError
from typing import Optional

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
            return {"message": "Product created succesfully", "user":new_product}
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
