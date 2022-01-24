from fastapi import FastAPI, Path
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class user(BaseModel):
    userID: int
    userName: str
    balance: Optional[float] = 0.00

usersList = {}

@app.get("/")
def home():
    return{"Home Page"}

#functions for the users class
@app.post("/create_user/{userID}/{userName}/{balance}")
def create_user(userID: int, userName: str, balance: float = 0.00):
    if user.userID in usersList:
        return {"Error": "User ID has already been taken."}
    elif user.userName in usersList:
        return {"Error": "User name has already been taken."}

@app.get("/get_user/{userID}")
def get_user(userID: int, item: user):
    return usersList[userID]






uvicorn.run(app)