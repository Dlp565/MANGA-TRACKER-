import uuid
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
      
    name: str = Field(...)
    hashed_password: str = Field(...)
    
    

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "ExUser",
                "hashed_password": "ExPass"
            }
        }

class UserInDB(User):
    hashed_password: str = Field(...)

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username: str | None = None
