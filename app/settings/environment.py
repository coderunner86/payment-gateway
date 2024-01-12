import os

from dotenv import load_dotenv

load_dotenv()

settings = {
    "app": {
        "port": os.getenv("PORT"),
    },
}
