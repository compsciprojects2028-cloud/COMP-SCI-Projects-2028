from fastapi import FastAPI
#1 Create FastAPI instance

app = FastAPI()

#Defines a route
@app.get("/")
def read_root():
    #FastAPI automatically converts the returned python dictionary 
    #as JSON response
    return {"Message":"Hello World, This is Gbemiga's First FastAPI  app"}
@app.get("/welcome")
def welCome():
    return {"Welcome to My path"}
#You run the app by doing uvicorn main(filename):app(FastAPI instance name) --reload

#Fastapi a lightling fast ASGI(Asynchronous Server Gateway Interface) server that runs application

#To check docs, navigate to https://127.0.0.1:8000/docs
# see automatically generated, interactive API documentation, webbased UI to test endpoints from browser
#/ReDoc More proffesional structured layout for your API DOcumentation


