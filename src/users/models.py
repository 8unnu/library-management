from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(UserLogin):
    is_admin: bool = False
    quan_books_taken: int = 0