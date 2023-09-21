from db import db
from dotenv import dotenv_values
from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from userModels import User
from collectionModels import *
from userRoutes import get_current_user
from isbn import *
import bson
from bson.json_util import dumps, loads

config = dotenv_values(".env")
router = APIRouter()

def setup_db_collection():
    collections = db["COLLECTIONS"]
    return collections

def setup_db_volume():
    volumes = db["VOLUMES"]
    return volumes

def setup_user():
    return db["USERS"]


async def get_user_collection_helper(user):
    collections = setup_db_collection()
    #finds collection based on user's name
    
    collections = collections.find({"userid":str(user["_id"])})
    col_list = list(collections)
    for col in col_list:
        del col['_id']
    return col_list

async def insert_volume(volume):

    volumes =  setup_db_volume()
    ret = volumes.find_one({"isbn":volume.isbn})
    if not ret:
        ret = volumes.insert_one(volume.model_dump())
        ret = volumes.find_one({"isbn":volume.isbn})
    return ret['_id']
    
def get_mal_link(series):
    return ''

async def add_volume_to_collection_helper(volume,volume_id,user):
    collections = setup_db_collection()
    
    collection_entry = collections.find_one({'series':volume.series, 'userid':str(user)})
    
    if not collection_entry:
        collectiondict = {}
        collectiondict['link'] = get_mal_link(volume.series)
        collectiondict['series'] = volume.series
        collectiondict['author'] = volume.author
        collectiondict['userid'] = str(user)
        collectiondict['volumes'] = []
        collection_model = CollectionEntry.parse_obj(collectiondict)
        
        ret = collections.insert_one(collection_model.model_dump())
        
        collection_entry = collections.find_one({'_id':ret.inserted_id})
    
    if not str(volume_id) in collection_entry['volumes']:
        collections.update_one({'series':volume.series, 'userid':str(user)},{'$push':{'volumes':str(volume_id)}})
    
    #see if this manga is in collection 

    #return collections.update_one({"user":user["name"]},{"$set": {'manga': manga}})


@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) :
    try:
        col = await get_user_collection_helper(current_user)
        return col
        #print(loads(col))
        #return loads(col)
        #returns Collection model from collection entry in DB
        #return Collection.model_validate(col)
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
async def add_volume_to_collection(current_user: Annotated[User, Depends(get_current_user)],volume: VolumeData = Depends()):
    #col = await get_user_collection_helper(current_user)
    volume_data = volume.model_dump()
    curr_volume = VolumeEntry.parse_obj(volume_data)
    volume_id = await insert_volume(curr_volume)
    await add_volume_to_collection_helper(volume,volume_id,current_user['_id'])

