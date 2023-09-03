from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import User

router = APIRouter()



@router.get("/users", response_description="Get all users", response_model = List[User])
def list_users(request: Request):
    # Error Here: 

    users = list(request.app.database["USERS"].find(limit=100))
    
    print(type(users[0]["_id"]))
    return users
    
@router.post("/register", response_description="POST user",status_code=status.HTTP_201_CREATED, response_model=User)
def create_test(request: Request, user: User = Body(...)):
    print(user)
    user = jsonable_encoder(user)
    new_user = request.app.database["USERS"].insert_one(user)
    created_user = request.app.database["USERS"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user


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