from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from userRoutes import router as user_router 
from dotenv import dotenv_values
config = dotenv_values(".env")



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
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router, tags=["users"], prefix="")

