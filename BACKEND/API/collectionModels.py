import uuid
from typing import Optional
from pydantic import BaseModel, Field, Json
from typing import List, Dict
from fastapi import Form
from mongoengine import *
from uuid import UUID, uuid4
from bson import ObjectId

class VolumeData(BaseModel):
    link: str
    series: str
    volume: str
    author: str
    image: str
    isbn: str
    language: str


class VolumeEntry(BaseModel):
    
    isbn: str
    link: str
    volume: str
    image: str
    language: str
    # @classmethod
    # def as_form(
    #     cls,
    #     link: str = Form(...),
    #     series: str = Form(...),
    #     volume: str = Form(...),
    #     author: str = Form(...),
    #     image: str = Form(...),
    #     isbn: str = Form(...),
    #     language: str = Form(...),
        
    # ) -> VolumeEntry:
    #     return cls(link=link,series=series,volume=volume,author=author,image=image,isbn=isbn,language=language)

class CollectionEntry(BaseModel):
    #name of manga
    series: str
    #author of manga
    author: str
    #link to mal of manga
    image: str
    genres: List[str]
    #list of isbns 
    userid: str
    volumes : Optional[List[str]]






"""
class Test(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "One Piece",
                "author": "Eiichiro Oda"
            }
        }
"""