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

async def insert_entry(user,manga):
    #TODO: Fix this 
    collections = setup_db()
    return collections.update_one({"user":user["name"]},{"$set": {'manga': manga}})


@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) -> Collection:
    try:
        col = await get_user_collection_helper(current_user)
        print(col)
        #returns Collection model from collection entry in DB
        return Collection.model_validate(col)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="collection could not be found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
#Used when user scans book (isnb) 
#Will result in various results that they could pick from
@router.get('/isbn')
async def get_volume_by_isbn(isbn: str):
    try:
        #volume may not contain actual volume num
        return getVolume(isbn)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get('/name')
async def get_volume_by_name(name: str):
    try:
        #volume may not contain actual volume num
        return getVolumeName(name)
    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post('/addCollection')
async def add_volume_to_collection(current_user: Annotated[User, Depends(get_current_user)],volume: VolumeEntry = Depends()):
    col = await get_user_collection_helper(current_user)
    print(col)
    if volume.series in col['manga']:
        currEntry = col['manga']      
    else:

        #TODO get mal link 
        mal_link = "filler"

        
        currEntry = {}
        currEntry['series'] = volume.series
        currEntry['author'] = volume.author
        currEntry['link'] = mal_link
        currEntry['volumes'] = []

        
    currEntry['volumes'].append(volume)
    entry = CollectionEntry.validate(currEntry)
    col['manga'][volume.series] = entry
    newCol = Collection.validate(col)
    manga = col['manga']
    print(manga)
    ret = await insert_entry(current_user,manga)
    print(ret)
    return {}
