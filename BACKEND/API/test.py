from pymongo import MongoClient
client = MongoClient('localhost',27017)

db = client["MANGA-TRACKER"]

users = db["USERS"]

test = {
    "name": "DLP",
    "password" : "M"
}

user_id = users.insert_one(test).inserted_id
print(user_id)

