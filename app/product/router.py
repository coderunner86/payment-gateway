from fastapi import APIRouter, HTTPException, Depends
from app.product.services import CreateProduct, UpdateProduct, ProductService

product_service = ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(product_service)]
)

@router.get("/{id:int}")
async def get_product(id: int, product_service: ProductService = Depends()):
    return await product_service.find_product(product_id=id)

@router.get("/all_products")
async def get_all_products(product_service: ProductService = Depends()):
    return await product_service.find_all_product()

@router.post("/new")
async def create_product(product: CreateProduct, product_service: ProductService= Depends()):
    try:
        new_product = await product_service.create_product(product)
        return new_product
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fuck! Internal Server Error: {str(ex)}")
    

@router.put("/{id}")
async def update_product(id: int, product: UpdateProduct, product_service:ProductService = Depends()):
    return await product_service.update_product(product_id=id, product=product)


@router.delete("/delete_product/{id}")
async def delete_product(id: int, product_service: ProductService = Depends()):
    return await product_service.delete_product(product_id=id)

@router.delete("/product/archive/{product_id}")
def archive_product_by_prod_id(product_id: str, product_service: ProductService = Depends()):
    try:
        archived_product = product_service.archive_by_prod_id(product_id=product_id)
        return {"message": "Product archived on stripe", "product": archived_product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error muy puto: {str(e)}")
