from db import db
from dotenv import dotenv_values
from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from userModels import User
from collectionModels import *
from userRoutes import get_current_user


config = dotenv_values(".env")
router = APIRouter()

def setup_db():
    users = db["COLLECTIONS"]
    return users

def get_user_collection(username):
    users = setup_db()
    u = users.find_one({"user":username})
    return u

@router.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    print(current_user)
    del current_user['_id']
    del current_user["hashed_password"]

    
    return current_user

@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) -> Collection:
    username = current_user['name']
    
