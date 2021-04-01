from fastapi import FastAPI, Query, Path, Body

from data_model import House, User
from shakes import Shake
from states_db import states_db

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/mycoolpage")
def root():
    return {"message": "Welcome to the cool page!"}


@app.get("/items/{name}")
async def read_item(name):  # query
    return {"message": f"you found the {name}"}


@app.get("/integers_only/{i}")
async def read_item(i: int):
    return {"message": i}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "nice to meet me!"}


@app.get("/users/{user_id}")
async def read_user(user_id: int = Path(..., title="User ID", ge=1)):
    # don't put this before users/me!
    return {"user_id": f"nice to meet you, clone {user_id}"}


@app.get("/shakes/{flavor}")
async def get_shake(flavor: Shake):
    if flavor == Shake.MINT:
        return {
            "flavor": flavor.name,
            "message": "A milkshake preserved for years in mint condition.",
        }
    if flavor == Shake.COOKIES:
        return {
            "flavor": flavor.name,
            "message": "I follow internet privacy guidelines by clearing the cookies "
            "from my fridge.",
        }
    if flavor == Shake.VANILLA:
        return {
            "flavor": flavor.name,
            "message": "Why did they name this flavor after a synonym for boring?",
        }
    if flavor == Shake.CHOCOLATE:
        return {"flavor": flavor.name, "message": "I kill dogs."}


@app.get("/state_abbrevs/")
async def read_item(
    name,
    news_source: str = Query(
        ..., title="news_source", alias="news-source", max_length=20
    ),
    date: str = Query("2020", deprecated=True),
):
    if name.upper() in states_db:
        return {
            "message": f"BREAKING NEWS FROM {news_source.upper()}: {name.title()} has "
            f"voted to secede from the union!"
        }
    else:
        return {
            "message": f"The movement for {name.upper()} to join the union still needs "
            f"your support! Sign up now at {news_source.lower()}.com"
        }


@app.get("/lights/")
async def read_item(status: bool):
    if status:
        return {"message": f"The light is on, but it's still dark in here."}
    else:
        return {"message": f"Could someone turn on the light?"}


@app.post("/houses/")
async def create_item(house: House):
    house = house.dict()
    if house["sqft"] != 0:
        house.update({"price_per_sqft": house["price"] / house["sqft"]})
    else:
        house.update({"price_per_sqft": None})
    return house


@app.put("/buyahouse/{item_id}")
async def update_item(
    item_id: int,
    user: User,
    house: House = Body(
        ...,
        example={
            "name": "Seinfeld Apartment",
            "address": "Apartment 5A, 129 W. 81st St., New York, N.Y.",
            "price": 1000,
            "sqft": 300,
        },
    ),
    bid: int = Body(..., embed=True),
):
    results = {"item_id": item_id, "house": house, "user": user, "bid": bid}
    return results
