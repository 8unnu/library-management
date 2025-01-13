from fastapi import APIRouter, Depends, Response

from src.database.database import session_maker, User
from src.database.utils import get_all_usernames, get_user_password
from src.users.models import UserRegister, UserLogin
from src.users.utils import encode_jwt

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
    with session_maker() as db:
        try:
            user = User(username=userdata.username, password=userdata.password, is_admin=userdata.is_admin,
                        quan_books_taken=userdata.quan_books_taken)
            db.add(user)
            db.commit()
            return {"message": "Пользовател создан"}
        except Exception as exc:
            print(exc)
    return


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