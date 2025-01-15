from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(UserLogin):
    is_admin: bool = False
    quan_books_taken: int = 0


class UserEdit(BaseModel):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    quan_books_taken: Optional[int] = None