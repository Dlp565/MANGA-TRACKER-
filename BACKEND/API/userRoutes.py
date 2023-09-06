from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Annotated
from userModels import User, UserInDB, Token, TokenData
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import dotenv_values
from pymongo import MongoClient
config = dotenv_values(".env")


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def setup_db():
    client = MongoClient(config["ATLAS_URI"])
    db = client[config["DB_NAME"]]
    users = db["USERS"]
    return users

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

@router.post("/token")
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
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
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

@router.get('/items/')
async def read_items(token: Annotated[str, Depends(get_current_active_user)]):
    return {"token": token}

@router.get('/users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    print(current_user)
    del current_user['_id']
    del current_user["hashed_password"]

    
    return current_user



'''

@router.get("/users", response_description="Get all users", response_model = List[User])
def list_users(request: Request):
    # Error Here: 

    users = list(request.app.database["USERS"].find(limit=100))
    
    print(type(users[0]["_id"]))
    return users
    
@router.post("/register", response_description="POST user",status_code=status.HTTP_201_CREATED, response_model=User)
def create_test(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["USERS"].insert_one(user)
    created_user = request.app.database["USERS"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


'''
'''
@router.post("/", response_description="Test POST",status_code=status.HTTP_201_CREATED, response_model=Test)
def create_test(request: Request, test: Test = Body(...)):
    test = jsonable_encoder(test)
    new_test = request.app.database["test"].insert_one(test)
    created_test = request.app.database["test"].find_one(
        {"_id": new_test.inserted_id}
    )

    return created_test

@router.get("/", response_description="Get all tests", response_model = List[Test])
def list_tests(request: Request):
    tests = list(request.app.database["tests"].find(limit=100))
    return tests

@router.get("/{id}", response_description="Get a single test by id", response_model=Test)
def find_book(id: str, request: Request):
    if (test := request.app.database["tests"].find_one({"_id":id})) is not None:
        return test
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Test with ID {id} not found' )

'''