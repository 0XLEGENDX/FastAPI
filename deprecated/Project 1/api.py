from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [ 
    {"title": "Title One", "author" : "Author One", "category": "science"},
    {"title": "Title Two", "author" : "Author Two", "category": "science"},
    {"title": "Title Three", "author" : "Author Three", "category": "science"},
    {"title": "Title Four", "author" : "Author Four", "category": "science"},
    {"title": "Title Five", "author" : "Author Five", "category": "science"},
    {"title": "Title Six", "author" : "Author Six", "category": "science"}
    ]


@app.get("/api-endpoint")
async def first_api():
    return {"message" : "Hello! Anurag"}

@app.get("/read-all-books")
async def first_api():
    return BOOKS

@app.get("/books/mybook")
async def fetch_all_books():
    return BOOKS[0]

@app.get("/books/{book_author}")
async def read_category_by_query(book_author: str,category: str):

    books_to_return = []

    for book in BOOKS:
        if(book["category"].casefold() == category.casefold() and book_author.casefold() == book["author"].casefold()):
            books_to_return.append(book)
        
    return books_to_return

@app.get("/books/{book_name}")
async def fetch_all_books(book_name : str):
    if(book_name):
        return {"dynamic_param": book_name}
    return BOOKS


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    try:
        BOOKS.append(new_book)
        return {"status" : "Added Book"}
    except:
        return {"status" : "Error In Adding Book"}


@app.put("/books/updatebook")
async def update_book(book_body = Body()):
    
    for index, item in enumerate(BOOKS):

        if(item.get("title").casefold() == book_body.get("title").casefold()):
            BOOKS[index] = book_body

    return BOOKS

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title):

    for index, element in enumerate(BOOKS):
        if(book_title == element.get("title")):
            BOOKS.pop(index)
    return BOOKS


@app.get("/read_all_books/{author_name}")
async def read_all_author_books(author_name:str):

    author_books = []
    for index, element in enumerate(BOOKS):

        if(element.get("author").casefold() == author_name.casefold()):
            author_books.append(element)

    return author_books 