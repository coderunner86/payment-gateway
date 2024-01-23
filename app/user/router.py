from fastapi import APIRouter, HTTPException, Depends

from app.user.services import CreateUser, UpdateUser, UserService
from app.stripe_integration.stripe_users import delete_stripe_customer
user_service = UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(user_service)]
)

@router.get("/{id:int}")
async def get_user(id: int, user_service: UserService = Depends()):
    return await user_service.find_user(user_id=id)


@router.get("/{email:str}")
async def get_user_by_email(email: str, user_service: UserService = Depends()):
    return await user_service.find_user_by_email(email=email)

@router.get("/user_id_by_cus/{cus_id:str}")
async def get_user_id(cus_id: str, user_service: UserService = Depends()):
    result = await user_service.find_user_id_by_cus(cus_id=cus_id)
    result = {"user_id": result}
    print(type(result), result)
    return result

@router.get("/user_cus_by_id/{user_id:int}")
async def get_user_cus(user_id: int, user_service: UserService = Depends()):
    result = await user_service.find_user_cus_by_id(user_id=user_id)
    result = {"user_id": result}
    print(type(result), result)
    return result

@router.get("")
async def get_all_users(user_service: UserService = Depends()):
    return await user_service.find_all_user()

@router.post("/new")
async def create_user(user: CreateUser, user_service: UserService=Depends()):
    try:
        new_user = await user_service.create_user(user)
        return new_user
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fuck! Internal Server Error: {str(ex)}")

@router.put("/{id}")
async def update_user(id: int, user: UpdateUser, user_service:UserService = Depends()):
    return await user_service.update_user(user_id=id, user=user)


@router.delete("/{id}")
async def delete_user(id: int, user_service: UserService = Depends()):
    return await user_service.delete_user(user_id=id)

@router.delete("/delete_by_cus/{customer_id}")
async def delete_customer(customer_id: str):
    try:
        deleted_customer = delete_stripe_customer(customer_id)
        return {"message": "Customer deleted successfully", "customer": deleted_customer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting customer: {str(e)}")