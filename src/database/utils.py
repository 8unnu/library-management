from sqlalchemy import inspect, Date
from sqlalchemy.sql import select
from src.database.database import (session_maker,
                                   Author, Book,
                                   BorrowedBook, User)


# users ________________________________________________________________________________________________________________
async def add_user(userdata):
    with session_maker() as db:
        try:
            user = User(username=userdata.username, password=userdata.password, is_admin=userdata.is_admin,
                        quan_books_taken=userdata.quan_books_taken)
            db.add(user)
            db.commit()
            return {"message": "Пользовател создан"}
        except Exception as exc:
            print(exc)

async def get_all_usernames():
    with session_maker() as db:
        users = db.query(User).all()
        try:
            usernames = [u.username for u in users]
            return usernames
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def get_user_password(username):
    with session_maker() as db:
        try:
            user = db.query(User).filter(User.username == username).first()
            return user.password
        except Exception as exc:
            print(f"Error: {exc}")


async def get_user_role(username):
    with session_maker() as db:
        try:
            user = db.query(User).filter(User.username == username).first()
            return user.is_admin
        except Exception as exc:
            print(f"Error: {exc}")


async def edit_user_data(username, userdata):
    with session_maker() as db:
        try:
            user = db.query(User).filter(User.username == username)
            user_columns = user.statement.columns.keys()[2:]

            for column, value in zip(user_columns, userdata.values()):
                if value:
                    user.update({f"{column}": value})

            db.commit()
        except Exception as exc:
            print(f"Error: {exc}")


# authors ______________________________________________________________________________________________________________

async def get_all_authors():
    with session_maker() as db:
        authors = db.query(Author).all()
        try:
            authors_names = [a.name.capitalize() for a in authors]
            return authors_names
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def add_author(author_data):
    with session_maker() as db:
        try:
            author = Author(name=author_data.name, biography=author_data.biography, birthday=author_data.birthday)
            db.add(author)
            db.commit()
        except Exception as exc:
            print(f"Error: {exc}")


async def get_author_data(author_name):
    with session_maker() as db:
        try:
            author = db.query(Author).filter(Author.name == author_name).first()
            author_data = {
                "name": author.name,
                "biography": author.biography,
                "birthday": author.birthday.date()
            }
            return author_data
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def edit_author_data(author_name, author_data):
    with session_maker() as db:
        try:
            author = db.query(Author).filter(Author.name == author_name)
            author_columns = author.statement.columns.keys()[2:]
            for column, value in zip(author_columns, author_data.values()):
                if value:
                    author.update({f"{column}": value})
            db.commit()
        except Exception as exc:
            print(f"Error: {exc}")

# books ________________________________________________________________________________________________________________


async def get_all_books():
    with session_maker() as db:
        books = db.query(Book).all()
        try:
            books_titles = [b.title.capitalize() for b in books]
            return books_titles
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def add_book(book_data):
    with session_maker() as db:
        try:
            book = Book(title=book_data.title, description=book_data.description, author=book_data.author,
                        genre=book_data.genre, quantity=book_data.quantity)
            db.add(book)
            db.commit()
        except Exception as exc:
            print(f"Error: {exc}")


async def get_book_data(book_title):
    with session_maker() as db:
        try:
            book = db.query(Book).filter(Book.title == book_title).first()
            book_data = {
                "title": book.title,
                "description": book.description,
                "publish_date": book.publish_date.date(),
                "author": book.author,
                "genre": book.genre,
                "quantity": book.quantity,
            }
            return book_data
        except Exception as exc:
            print(f"Error: {exc}")
            return []


async def edit_book_data(book_title, book_data):
    with session_maker() as db:
        try:
            book = db.query(Book).filter(Book.title == book_title)
            book_columns = [b_c for b_c in book.statement.columns.keys()[2:] if b_c != "publish_date"]
            for column, value in zip(book_columns, book_data.values()):
                if value:
                    book.update({f"{column}": value})
            db.commit()
        except Exception as exc:
            print(f"Error: {exc}")