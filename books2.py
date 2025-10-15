from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Book:

    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating



class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,lt=6)


    model_config = {

        "json_schema_extra" : {

            "example" : {

                "title": "A new book",
                "author": "codingwithanurag",
                "description": "A new description of a book",
                "rating": 5
            }

        }
    } 



BOOKS = [

    Book(1,"Computer Science Pro","codingwithanurag","A very nice book!",5),
    Book(2,"Be Fast with FastAPI","codingwithanurag","A great book!",5),
    Book(3,"Maste Endpoints","codingwithanurag","A awesome book!",5),
    Book(4,"HP1","Author 1","A very nice book!",2),
    Book(5,"HP2","Author 2","A very nice book!",3),
    Book(6,"HP3","Author 3","A very nice book!",1) 

]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    
    new_book = Book(**book_request.model_dump())
    BOOKS.append( find_book_id(new_book) )
    return {"message": "success"}


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    books_list = []
    for book in BOOKS:
        if book.id == book_id:
            books_list.append(book)
    
    return books_list


@app.get("/books/")
async def read_book_by_rating(rating: int = Query(gt=0,lt=6)):

    books_list = []
    for book in BOOKS:
        if(book.rating == rating):
            books_list.append(book)
    
    return books_list

@app.put("/books/update_book")
async def update_book(book_json: BookRequest):

    book_json = Book(**book_json.model_dump())

    for index, book in enumerate(BOOKS):

        if(book.id == book_json.id):

            BOOKS[index] = book_json
        
    return {"message" : "success"}


@app.delete("/books/{book_id}")
async def delte_book_by_book_id(book_id: int):

    # items_to_delete = []
    flag = False
    for index, item in enumerate(BOOKS):

        if(item.id == book_id):
            flag = True
            BOOKS.pop(index)
            break
        
    response = {"status" : flag} 
    if(not flag):
        response["message"] = "Book not found"
    return response

        
            



def find_book_id(book: Book):

    if(len(BOOKS) > 0):
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book