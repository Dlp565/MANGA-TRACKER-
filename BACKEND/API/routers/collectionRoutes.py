from utils.db import db
from dotenv import dotenv_values
from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from models.userModels import User
from models.collectionModels import *
from routers.userRoutes import get_current_user
from utils.isbn import *
import bson
from utils.collectionFunctions import get_user_collection_helper, insert_volume, add_volume_to_collection_helper, remove_volume, get_volume

config = dotenv_values(".env")
router = APIRouter()
  
@router.patch('/removeVolume')
async def remove_volume_collection(current_user: Annotated[User, Depends(get_current_user)], volumeid : str, series: str):
    await remove_volume(volumeid,series,current_user['_id'])
    return {"Response": "Sucessfully Deleted Volume"}

@router.get('/volumes')
async def  getVolumes(current_user: Annotated[User, Depends(get_current_user)],volumeid: str) -> VolumeEntry | None:
    return await get_volume(volumeid=volumeid)


@router.get('/mycollection')
async def get_user_collection(current_user: Annotated[User, Depends(get_current_user)]) :
    try:
        col = await get_user_collection_helper(current_user)
        return {"collection": col}
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
        ret,count = getVolumeName(name)
        
        rets = []
        for i in range(0,count):
            volume = ret[i]
            print(volume)
            try:
                VolumeEntry.parse_obj(volume)
                rets.append(volume)
            except Exception:
                print()
        return {"results": rets }

    except Exception as e:
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

#= Depends() 
@router.post('/addCollection')
async def add_volume_to_collection(current_user: Annotated[User, Depends(get_current_user)],volume: VolumeData ):
    #col = await get_user_collection_helper(current_user)
    volume_data = volume.model_dump()
    curr_volume = VolumeEntry.parse_obj(volume_data)
    volume_id = await insert_volume(curr_volume)
    await add_volume_to_collection_helper(volume,volume_id,current_user['_id'])

