from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List, Annotated
from models.userModels import User, TokenData
from jose import jwt
from passlib.context import CryptContext
from dotenv import dotenv_values
from utils.users import *
config = dotenv_values(".env")


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




@router.post("/login")
async def login_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    #authenticates the user 
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    # set access token expiration date using env preset amount
    access_token_expires = timedelta(weeks=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    # create the access token 
    access_token = create_access_token(
        data={"sub": user["name"]}, expires_delta=access_token_expires
    )
    
    print(access_token)
    # sends the access token 
    #return {"access_token" : user["name"], "token_type": "bearer"}
    return {"access_token" : access_token, "token_type": "bearer"}


@router.post('/register')
async def register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) :
    user = get_user(form_data.username)
    if user:
        raise HTTPException(status_code=409, detail="User with this username already exists")
    user = create_user(form_data.username,form_data.password)

    

    

    # set access token expiration date using env preset amount
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    # create the access token 
    access_token = create_access_token(
        data={"sub": user["name"]}, expires_delta=access_token_expires
    )

   # sends the access token 
    #return {"access_token" : user["name"], "token_type": "bearer"}
    return {"access_token" : access_token, "token_type": "bearer"}





