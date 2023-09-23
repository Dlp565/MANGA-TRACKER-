from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import  Annotated
from models.userModels import User, TokenData
from jose import jwt
from passlib.context import CryptContext
from dotenv import dotenv_values
from utils.db import db

config = dotenv_values(".env")


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def setup_db():
    users = db["USERS"]
    return users

def setup_collection():
    collections = db["COLLECTIONS"]
    return collections

def verify_password(plain_password, hashed_password):
    

    # Ensures the hashed password and plain password are the same
    return pwd_context.verify(plain_password,hashed_password)
    
def get_password_hash(password):

    # Returns the hash for a password

    return pwd_context.hash(password)

def get_user(username: str):
    
   # Get user from database
        # this one needs to change to get the user from the database 

    
    users = setup_db()
    u = users.find_one({"name":username})
    return u
    
def create_user(username: str, password: str):
    users = setup_db()
    u = users.insert_one({"name":username,"hashed_password":get_password_hash(password)})
    return get_user(username)
    

def authenticate_user(username: str, password: str):
    # checks that user login (w/ username + password) are in the DB
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data:dict, expires_delta: timedelta | None = None):

    # Creates an access token with expiration date 

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,config["SECRET_KEY"],algorithm=config["ALGORITHM"])
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    #function to get current user 


    # prewritten exception when credentials are wrong
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        #take in the token and decode it using the secret key and algo
        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=config["ALGORITHM"])
        #get the username from the decoded token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        #store TokenData as it's own thing
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception

    #get user from db based on username from token

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user 

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user