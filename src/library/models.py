from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AuthorAdd(BaseModel):
    name: str
    biography: str
    birthday: datetime


class AuthorEdit(BaseModel):
    biography: Optional[str] = None
    birthday: Optional[datetime] = None


class BookAdd(BaseModel):
    title: str
    description: str
    author: str
    genre: str
    quantity: int

class BookEdit(BaseModel):
    description: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    quantity: Optional[int] = None