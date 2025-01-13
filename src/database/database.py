from sqlalchemy import (create_engine, func,
                        Boolean, DateTime, Column, Integer, String, ForeignKey)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import (DB_USER, DB_PASSWORD,
                        DB_HOST, DB_PORT,
                        DB_NAME)

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(url=DATABASE_URL)
session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# models _______________________________________________________________________________________________________________


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    quan_books_taken = Column(Integer, default=0)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    biography = Column(String)
    birthday = Column(DateTime())


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    publish_date = Column(DateTime(timezone=True), server_default=func.now())
    author = Column(String, ForeignKey("authors.name"))
    genre = Column(String)
    quantity = Column(Integer)

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String, ForeignKey("users.username"))
    book_title = Column(String, ForeignKey("books.title"))
    taken_date = Column(DateTime(timezone=True), server_default=func.now())
    back_date = Column(DateTime())

