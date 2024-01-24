import os
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()

secretKey = os.getenv("SECRET_KEY")


def create_token(data: dict) -> str:
    """
    Create a token based on the input data using the provided secret key and algorithm.

    Args:
        data (dict): The data to be encoded into the token.

    Returns:
        str: The generated token.
    """
    token: str = encode(payload=data, key=secretKey, algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    """
    Validates the given token.

    Args:
        token (str): The token to validate.

    Returns:
        dict: The decoded data from the token.
    """
    data: dict = decode(token, key=secretKey, algorithms=["HS256"])
    return data
