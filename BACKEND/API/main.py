from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from routers.userRoutes import router as user_router 
from routers.collectionRoutes import router as collection_router
from dotenv import dotenv_values
config = dotenv_values(".env")
import uvicorn
import os, sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,project_root)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup_db_client(request = Request):
    print(config["ATLAS_URI"])
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    #app.mongodb_client = MongoClient("localhost",27017)
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Conneceted to the MongoDB DB!")
    print(sys.path)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router, tags=["users"], prefix="")
app.include_router(collection_router, tags = ["collection"],prefix = "/collection")

@app.get('/home')
def test():
    return "works!"
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload = 'True')
