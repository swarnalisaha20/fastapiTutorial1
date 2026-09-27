from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from pydantic import BaseModel
import models


# Note:
# In Laravel, if you want something to happen when your application boots up, 
# you might put it in the boot() method of a Service Provider. In FastAPI, we use this lifespan function for that exact same purpose.

# 1. This function runs right before the server starts
#asynccontextmanager - This is a special Python tag. It tells FastAPI: 
# "Hey, this function handles the entire life of the app (from the moment it starts, to the moment it stops)."
@asynccontextmanager 
async def lifespan(app: FastAPI):
    print("Server is starting... creating tables!")
    # This is the magic command that creates your database tables:
    async with engine.begin() as conn:
        #makes connectiom
        await conn.run_sync(models.Base.metadata.create_all) #models.Base.metadata holds list of models, create_all makes table if doesn't exist
    print("Tables created successfully!")
    yield 
    # This tells FastAPI to continue starting the server 
    #yield This is a special Python keyword. It essentially means:
    #  "Okay, we finished the setup. Pause this function right here and
    #  let the web server start running for the users!" (Fun fact: If you ever press Ctrl+C to kill your server, FastAPI will come right back to this yield line and run any code you put below it to clean things up).



# 2. Add the lifespan to your app
app = FastAPI(lifespan=lifespan)


# Tutorial 1
# app = FastAPI()


# # 1. Create a Pydantic Model (This acts like a Laravel Form Request)
# class Item(BaseModel):
#     name:str
#     price:float
#     description:str | None=None # This means 'description' is optional


# #Eg. of route define
# @app.get("/")
# def home():
#     return {"message": "Hello World"}


# # 2. Create a POST route to receive data
# @app.post("/items/")
# def create_item(item: Item):
#     # FastAPI automatically checks if 'name' is a string and 'price' is a float!
#     # If the user sends a string for price (like "ten"), FastAPI automatically throws a 422 Error
#     return {
#         "success": True,
#         "message": f"Item {item.name} created",
#         "price": item.price
#     }