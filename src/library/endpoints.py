from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import RedirectResponse

from src.database.utils import get_all_usernames
from src.users.utils import decode_jwt

library_router = APIRouter(
    prefix='/library',
    tags=['library']
)


@library_router.get("/")
async def index(users: dict = Depends(get_all_usernames),
                access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users:
        return {"message": "Добро пожаловать в библиотеку"}
    else:
        return RedirectResponse("/users")