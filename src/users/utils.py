import jwt

from src.config import SECRET_KEY
from src.config import ALGORITHM


async def encode_jwt(data: dict):
    return jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)

async def decode_jwt(token):
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    except Exception:
        return {"sub": "None"}
