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
    """
    Asynchronous function to retrieve a user ID based on a customer ID.

    Parameters:
    - cus_id: a string representing the customer ID
    - user_service: an instance of UserService, provided as a dependency

    Returns:
    - A dictionary containing the user ID
    """
    result = await user_service.find_user_id_by_cus(cus_id=cus_id)
    result = {"user_id": result}
    print(type(result), result)
    return result

@router.get("/user_cus_by_id/{user_id:int}")
async def get_user_cus(user_id: int, user_service: UserService = Depends()):
    """
    Retrieve user custom data by user ID.

    Args:
        user_id (int): The ID of the user.
        user_service (UserService, optional): The user service to use for data retrieval.

    Returns:
        dict: A dictionary containing the user ID and the custom data.
    """
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
    """
    Asynchronous function to delete a user by ID using the provided user_service.

    Args:
        id (int): The ID of the user to be deleted.
        user_service (UserService, optional): The user service to use for deleting the user. Defaults to Depends().

    Returns:
        The result of the user_service.delete_user method.
    """
    return await user_service.delete_user(user_id=id)

@router.delete("/delete_by_cus_on_table/{cus_id}")
async def delete_stripe_user_on_table(cus_id: str, user_service: UserService = Depends()):
    """
    Deletes a stripe user on the table by customer ID.

    Args:
        cus_id (str): The ID of the customer to be deleted.
        user_service (UserService, optional): The user service dependency. Defaults to None.

    Returns:
        The result of deleting the stripe user on the table.
    """
    return await user_service.delete_stripe_user_on_table(cus_id=cus_id)

@router.delete("/delete_by_cus_on_stripe/{customer_id}")
async def delete_customer(customer_id: str):
    """
    Deletes a customer by their ID on the Stripe platform.

    Args:
        customer_id (str): The ID of the customer to be deleted.

    Returns:
        dict: A dictionary containing the message "Customer deleted successfully" and the deleted customer details.

    Raises:
        HTTPException: If an error occurs while deleting the customer.
    """
    try:
        deleted_customer = delete_stripe_customer(customer_id)
        return {"message": "Customer deleted successfully", "customer": deleted_customer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting customer: {str(e)}")