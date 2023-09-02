from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as test_router 
config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Conneceted to the MongoDB DB!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(test_router, tags=["tests"], prefix="/test")

'''

FastAPI first Tutorial 

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id:int, q: Union[str,None] = None):
    return {"item_id": item_id, "q":q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name" : item.name, "item_id": item_id}
'''