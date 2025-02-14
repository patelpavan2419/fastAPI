from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional
# from datetime import datetime


app = FastAPI()
current_id = 1
class Book:
    id: Optional[int] = None
    title: str 
    author: str
    category: str 
    published_date: str 

    def __init__(self, title, author, category, published_date,  id: Optional[int] = None):
        global current_id
        self.id=id or current_id
        self.title=title
        self.author=author
        self.category=category
        self.published_date = published_date
        current_id += 1

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=15)
    category: str = Field(min_length=3, max_length=25)
    published_date: str 

    class Config: 
        json_schema_extra = {
            "example": {
                "title": 'A new Book Name',
                "author": 'AutherName',
                "category": 'A new Book category',
                "published_date": "2022"
            }
        }

BOOKS = [
    Book('Title Two', 'Author Two', 'science', '2001'),
    Book('Title Three', 'Author Three', 'history', '1995'),
    Book('Title Four', 'Author Four', 'math', '2002'),
    Book('Title Five', 'Author Five', 'math', '2022'),
    Book('Title Six', 'Author Two', 'CSS', '2200')
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}") # here "book_title" is passed as dynamic param
async def read_book(book_title: str):
    for book in BOOKS:
        if book.title.casefold() == book_title.casefold():
            return book

@app.get("/books/id/{book_id}") # here "book_id" is passed as dynamic param
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/published_date/{year}") # here "book_id" is passed as dynamic param
async def read_book(year: str):
    for book in BOOKS:
        if book.published_date == year:
            return book


@app.get("/books/")
async def read_category_by_query(category: str):  # query param
    books_to_return = []
    for book in BOOKS:
        if book.category.casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str): # query param
    books_to_return = []
    for book in BOOKS:
        if book.author.casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/") # dynamic param or Path Parameter
async def read_author_category_by_query(book_author: str, category: str): # here "category" is query param & "book_author" is dynamic param
    books_to_return = []
    for book in BOOKS:
        if book.author.casefold() == book_author.casefold() and \
                book.category.casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(book_request: BookRequest): # request body
    new_book = Book(**book_request.dict())
    BOOKS.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


@app.put("/books/update_book")
async def update_book(updated_book: BookRequest): # request body
    updateBook = Book(**updated_book.dict())
    for i in range(len(BOOKS)):
        if BOOKS[i].title.casefold() == updateBook.title.casefold():
            BOOKS[i] = updateBook
    return {"message": "Book updated successfully", "book": updateBook}


@app.delete("/books/delete_book/{book_title}") # dynamic param
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].title.casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
