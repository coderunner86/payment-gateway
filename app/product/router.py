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
    

@router.put("/update/{id}")
async def update_product(id: int, product: UpdateProduct, product_service:ProductService = Depends()):
    return await product_service.update_product(product_id=id, product=product)


@router.delete("/delete_product/{id}")
async def delete_product(id: int, product_service: ProductService = Depends()):
    return await product_service.delete_product(product_id=id)

@router.delete("/product/archive/{product_id}")
def archive_product_by_prod_id(product_id: str, product_service: ProductService = Depends()):
    """
    Delete a product by its product ID and return a message along with the archived product.
    
    Args:
        product_id (str): The ID of the product to be archived.
        product_service (ProductService, optional): An instance of ProductService. Defaults to Depends().
    
    Returns:
        dict: A dictionary containing a message and the archived product.
    
    Raises:
        HTTPException: An exception with status code 500 and error message.
    """
    try:
        archived_product = product_service.archive_by_prod_id(product_id=product_id)
        return {"message": "Product archived on stripe", "product": archived_product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error muy puto: {str(e)}")

@router.put("/product/unarchive/{product_id}")
def unarchive_product_by_prod_id(product_id: str, product_service: ProductService = Depends()):
    """
    Endpoint to unarchive a product by its product ID.
    
    Args:
        product_id (str): The ID of the product to be unarchived.
        product_service (ProductService, optional): An instance of ProductService. Defaults to Depends().
    
    Returns:
        dict: A dictionary containing a message and the unarchived product.
    
    Raises:
        HTTPException: An error occurred during the unarchiving process.
    """
    try:
        unarchived_product = product_service.unarchive_by_prod_id(product_id=product_id)
        return {"message": "Product unarchived on stripe", "product": unarchived_product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error muy puto: {str(e)}")