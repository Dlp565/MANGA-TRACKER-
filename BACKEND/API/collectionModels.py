import uuid
from typing import Optional
from pydantic import BaseModel, Field, Json
from typing import List
class CollectionEntry(BaseModel):
    name: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    link: Optional[str]
    volumes : Optional[List[int]]

class Collection(BaseModel):
      
    user: str
    manga: List[CollectionEntry] = None
    
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user": "ExUser",
                "manga": ["entry","entry"]
            }
        }




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