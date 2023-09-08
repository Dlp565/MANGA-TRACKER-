from db import db
from dotenv import dotenv_values
from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from userModels import User
from collectionModels import *
from userRoutes import get_current_user
from isbn import *


config = dotenv_values(".env")
router = APIRouter()

def setup_db():
    collections = db["COLLECTIONS"]
    return collections

async def get_user_collection_helper(user):
    collections = setup_db()
    #finds collection based on user's name
    return collections.find_one({"user":user["name"]})




@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) -> Collection:
    try:
        col = await get_user_collection_helper(current_user)
        #returns Collection model from collection entry in DB
        return Collection.model_validate(col)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="collection could not be found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.get('/isbn')
async def get_user_collection(isbn: str):
    try:
        #volume may not contain actual volume num
        return getVolume(isbn)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )