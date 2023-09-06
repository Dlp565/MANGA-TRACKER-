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
    collections = db["COLLECTIONS"]
    return collections

async def get_user_collection_helper(user):
    collections = setup_db()
    return collections.find_one({"user":user["name"]})

@router.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    print(current_user)
    del current_user['_id']
    del current_user["hashed_password"]

    
    return current_user

@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) -> Collection:
    try:
        col = await get_user_collection_helper(current_user)
        print(col)
        return Collection.model_validate(col)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="collection could not be found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
