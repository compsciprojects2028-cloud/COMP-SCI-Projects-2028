#Pydantic is a python Library used for 
# data parsing and data validation using Python type hints.
#Validation If the client sends Data that doesn't match the pydantic model 
# (e.g they send "Two" instead of 2 for an int), Pydantic model immediately throws a clear validation error
#(HTTP 422), stopping the request before it hits your function logic.
#Serialization: It converts Python Objects into JSON and vice-versa
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#3 Define Pydantic model for a book
#This model inherits from BaseModel and uses python type hints for validation.
class Book(BaseModel):
    title:str #Must be a string
    author:str #Must be a string
    year:int #Must be a integer
    #optional field: using 'None' as default makes it optional
    isbn: str | None = None

#4 Create a POST endpoint that consumes the Pydantic Model
@app.post("/books/")    
def create_book(book:Book):# FastAPI expects a Book Object here
    #FastAPI automatically:
    # 1. Reads the JSON request body. 
    #2. Validates against book model
    #3 pases valid book object
    print(f"Received new book {book.title} by {book.author}")
    return {"status":"Book created", "data":book}
#Analogy Python is single threaded 
#await lets you switch while a task is cooking, making it never idle
#Uvicorn is the store manager /switchboard, Fastapi is the guy switching
#but the guy speaks in python(objects) the customer(web browser) HTTP
#uvicorn catches the customer coming in (HTTP request)
# it translates to the python form
#Uvicorn creates the socket, listens on the port, 
# parses raw HTTP bytes into ASGI scope and gives FastAPI app