from fastapi import APIRouter, Cookie, Depends

from src.database.utils import (add_author, edit_author_data, get_all_authors, get_author_data,
                                get_all_usernames, get_user_role,
                                add_book, edit_book_data, get_all_books, get_book_data, edit_book_quantity,
                                borrow_book, edit_borrow_book_quantity, get_borrow_books_titles)
from src.library.models import (AuthorAdd, AuthorEdit,
                                BookAdd, BookEdit, BookBorrow, BookBorrowBack)
from src.users.utils import decode_jwt


library_router = APIRouter(
    prefix='/library',
    tags=['library']
)


@library_router.get("/")
async def library(users: dict = Depends(get_all_usernames),
                  access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users:
        return {"message": "Добро пожаловать в библиотеку"}


# authors ______________________________________________________________________________________________________________


@library_router.get("/authors/")
async def authors(authors_names: dict = Depends(get_all_authors),
                  users: dict = Depends(get_all_usernames),
                  access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users:
        return {"message": authors_names}


@library_router.get("/authors/{author_name}")
async def author_getinfo(author_name: str,
                         authors_names: dict = Depends(get_all_authors),
                         users: dict = Depends(get_all_usernames),
                         access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users and author_name.capitalize() in authors_names:
        author_data = await get_author_data(author_name)
        return {"message": author_data}


@library_router.post("/authors/add")
async def author_add(author_data: AuthorAdd,
                     authors_names: dict = Depends(get_all_authors),
                     users: dict = Depends(get_all_usernames),
                     access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    is_admin = await get_user_role(username)
    if username in users and is_admin:
        if author_data.name.capitalize() not in authors_names:
            await add_author(author_data)
            return {"message": f"{author_data.name} добавлен"}


@library_router.patch('/authors/edit/{author_name}')
async def author_edit(author_name: str,
                      author_data: AuthorEdit,
                      authors_names: dict = Depends(get_all_authors),
                      users: dict = Depends(get_all_usernames),
                      access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    is_admin = await get_user_role(username)
    if (author_name.capitalize() in authors_names
            and username in users
            and is_admin):
        author_data = {key: value for key, value in author_data}
        await edit_author_data(author_name, author_data)
        return {"message": f"Данные {author_name} изменены"}


# books ________________________________________________________________________________________________________________


@library_router.get("/books/")
async def books(books_titles: dict = Depends(get_all_books),
                users: dict = Depends(get_all_usernames),
                access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users:
        return {"message": books_titles}


@library_router.get("/books/{book_title}")
async def book_getinfo(book_title: str,
                       books_titles: dict = Depends(get_all_books),
                       users: dict = Depends(get_all_usernames),
                       access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users and book_title.capitalize() in books_titles:
        book_data = await get_book_data(book_title)
        return book_data


@library_router.post("/books/get/{book_title}")
async def book_get(book_title: str,
                   borrowed_book_data: BookBorrow,
                   books_titles: dict = Depends(get_all_books),
                   users: dict = Depends(get_all_usernames),
                   access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    if username in users and book_title.capitalize() in books_titles:
        book_data = await get_book_data(book_title)
        if borrowed_book_data.quantity_book_taken <= book_data["quantity"]:
            await edit_book_quantity(book_title, borrowed_book_data.quantity_book_taken, operation="take")
            borrowed_book_data = {
                "username": username,
                "book_title": book_title,
                "back_date": borrowed_book_data.back_date,
                "quantity_book_taken": borrowed_book_data.quantity_book_taken
            }
            await borrow_book(borrowed_book_data)
            return {"message": f"Вы взяли {borrowed_book_data["quantity_book_taken"]} книг '{book_title}'"}


@library_router.post("/books/back/{book_title}")
async def book_back(book_title: str,
                    borrow_book_data: BookBorrowBack,
                    users: dict = Depends(get_all_usernames),
                    access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    borrow_books_titles = await get_borrow_books_titles(username, book_title)
    if username in users and book_title.capitalize() in borrow_books_titles:
        await edit_borrow_book_quantity(username, book_title, borrow_book_data.quantity_book_taken)
        await edit_book_quantity(book_title, borrow_book_data.quantity_book_taken, operation="back")
        return {"message": f"Было возвращено в библиотеку {borrow_book_data.quantity_book_taken} книг '{book_title}'"}


@library_router.post("/books/add")
async def book_add(book_data: BookAdd,
                   books_titles: dict = Depends(get_all_books),
                   authors_names: dict = Depends(get_all_authors),
                   users: dict = Depends(get_all_usernames),
                   access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    is_admin = await get_user_role(username)
    if username in users and is_admin:
        if (book_data.title.capitalize() not in books_titles
                and book_data.author.capitalize() in authors_names):
            await add_book(book_data)
            return {"message": f"Книга '{book_data.title.capitalize()}' добавлена в библиотеку"}


@library_router.patch('/books/edit/{book_title}')
async def book_edit(book_title: str,
                    book_data: BookEdit,
                    books_titles: dict = Depends(get_all_books),
                    authors_names: dict = Depends(get_all_authors),
                    users: dict = Depends(get_all_usernames),
                    access_token=Cookie(default=None)):
    payload = await decode_jwt(access_token)
    username = payload.get("sub")
    is_admin = await get_user_role(username)
    if (book_title.capitalize() in books_titles
            and book_data.author.capitalize() in authors_names
            and username in users
            and is_admin):
        book_data = {key: value for key, value in book_data}
        await edit_book_data(book_title, book_data)
        return {"message": f"Данные книги '{book_title.capitalize()}' изменены"}