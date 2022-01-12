import fastapi
import uvicorn
#yo matt, if you're testing this and it pops up a bunch of missing components or whatever,
    #click on terminal (very bottom of the IDE
    #type in "pip install fastapi" and then "pip install uvicorn"

api = fastapi.FastAPI()

#enter in endpoint /docs/ to get a listing of all endpoints in the api

#default endpoint or http page of our api
@api.get('/')
def index():
    return {
        "message": "Home page"
    }

@api.get('/user/')
def user():
    return{
        "message": "User page"
    }

"""
@api.get("/user/{userID}")
def get_userID(userID: str):
    #(WIP CODE)return userName[userID]
    #idea is to havea directory of users with their ID numbers
    #enter in ">web address</user/>userID< and it will load data based on that ID's account
    # like total funds and name tied to account
"""


uvicorn.run(api)