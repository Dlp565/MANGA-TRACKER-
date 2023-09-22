from db import db
from typing import List, Annotated
from userModels import User
from collectionModels import *

from isbn import *
import bson

def setup_db_collection():
    collections = db["COLLECTIONS"]
    return collections

def setup_db_volume():
    volumes = db["VOLUMES"]
    return volumes

def setup_user():
    return db["USERS"]

async def remove_volume(volumeid, series,user):
    collections = setup_db_collection()
    collection = collections.update_one({"userid":str(user),"series":series},
                                        {'$pull': {'volumes': str(volumeid)}})
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
    


async def add_volume_to_collection_helper(volume,volume_id,user):
    collections = setup_db_collection()
    
    collection_entry = collections.find_one({'series':volume.series, 'userid':str(user)})
    
    if not collection_entry:
        collectiondict = {}
        seriesInfo = {}
        try:
            seriesInfo = getSeries(volume.series)['data']['Media']
            collectiondict['image'] = seriesInfo['coverImage']['extraLarge']
            collectiondict['genres'] = seriesInfo['genres']
        
        except Exception:
            collectiondict['image'] = ''
            collectiondict['genres'] = []
        collectiondict['series'] = volume.series
        collectiondict['author'] = volume.author
        collectiondict['userid'] = str(user)
        collectiondict['volumes'] = []
        collection_model = CollectionEntry.parse_obj(collectiondict)
        
        ret = collections.insert_one(collection_model.model_dump())
        
        collection_entry = collections.find_one({'_id':ret.inserted_id})
    
    if not str(volume_id) in collection_entry['volumes']:
        collections.update_one({'series':volume.series, 'userid':str(user)},{'$push':{'volumes':str(volume_id)}})
    