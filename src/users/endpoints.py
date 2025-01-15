from fastapi import APIRouter, Cookie, Depends, Response

from src.database.database import session_maker, User
from src.database.utils import (add_user, edit_user_data, get_all_usernames,
                                get_user_password, get_user_role)
from src.users.models import UserRegister, UserLogin, UserEdit
from src.users.utils import encode_jwt, decode_jwt

users_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_router.get("/")
async def auth():
    return {"message": "Отправьте post-запрос на: /users/register - чтобы зарегистрироваться;"
                       " /users/login - чтобы залогиниться;"
                       " /users/logout - чтобы разлогиниться"}


@users_router.post("/register/")
async def register(userdata: UserRegister):
    await add_user(userdata)

@users_router.post("/login/")
async def login(response: Response,
                userdata: UserLogin,
                users: dict = Depends(get_all_usernames)):
    username = userdata.username
    correct_password = await get_user_password(username)
    if username in users and userdata.password == correct_password:
        token = await encode_jwt(data={"sub": username})
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"message": "Вы вошли в свой аккаунт"}


@users_router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы вышли из своего аккаунта"}


@users_router.patch('/edit/{username}')
async def edit(username: str,
               userdata: UserEdit,
               users: dict = Depends(get_all_usernames),
               access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    token_username = payload.get("sub")
    if username in users and username == token_username:
        is_admin = await get_user_role(username)
        if is_admin:
            userdata = {key: value for key, value in userdata}
        else:
            userdata = {key: value for key, value in userdata if key == "password"}
        await edit_user_data(username, userdata)
        return {"message": f"Данные пользователя {username} изменены"}