import os
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()

secretKey = os.getenv("SECRET_KEY")


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=secretKey, algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(token, key=secretKey, algorithms=["HS256"])
    return data