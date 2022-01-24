#To test api, go to terminal and type in "pip install fastapi" and then "pip install uvicorn"
from fastapi import FastAPI, Path
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

#data structures
class userID(BaseModel):
    userName: str
    balance: Optional[float] = 0.00


registeredUsers = {}

#default loading page
@app.get("/")
def home():
    return{"Home Page"}

#functions for the users class
@app.post("/create_user/{userID}")
def create_user(userID: int, item: userID):
    if userID in registeredUsers:
        return {"Error": "User ID already taken."}

    registeredUsers[userID] = {"userName": item.userName, "balance": item.balance}
    return registeredUsers[userID]

@app.get("/get_user/{userID}")
def get_user(userID: int):
    return registeredUsers[userID]






uvicorn.run(app)
#
# from fastapi import FastAPI, Path
# import uvicorn
# from typing import Optional
# from pydantic import BaseModel
#
# app = FastAPI()
#
# class Item(BaseModel):
#     name: str
#     price: float
#     brand: Optional[str] = None
#
# inventory = {
#     1: {
#         "name": "Milk",
#         "price": "3.99",
#         "brand": "regular"
#     }
# }
#
# @app.get("/")
# def home():
#     return {"Home Page"}
#
# @app.get("/about/")
# def about():
#     return {"Data": "About"}
#
# @app.get("/get_item/{itemID}")
# def get_item(itemID: int):
#     return inventory[itemID]
#
# @app.post("/create_item/{itemID}")
# def create_item (itemID: int, item: Item):
#     if itemID in inventory:
#         return {"Error": "Item ID already exists"}
#
#     inventory[itemID] = {"name": item.name, "price": item.price, "brand": item.brand,}
#     return inventory[itemID]
#
#
#
# uvicorn.run(app)