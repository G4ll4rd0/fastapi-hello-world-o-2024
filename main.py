'''
Main file to run example API
'''
import os
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyQuery
from pydantic import BaseModel

_ = load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_query = APIKeyQuery(name=API_KEY_NAME)

async def get_api_key(api_key: str = Security(api_key_query)) -> str:
    '''Confirms API_KEY exists

    Args:
        api_key (str, optional): Name to find api. Defaults to Security(api_key_query).

    Raises:
        HTTPException: Error 403, Lack of credentials

    Returns:
        str: api key stored in .env
    '''
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=403, detail="Could not validate credentials"
    )

class Item(BaseModel):
    '''
    _summary_
    '''
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/items/{item_id}")
async def read_item(item_id: int,
                    q: str | None = None,
                    api_key: str = Depends(get_api_key)) -> dict[str, Any]: # pylint: disable=unused-argument
    '''
    Endpoint to read items

    Args:
        item_id (int): ID of Item to read
        q (str, optional): _description_. Defaults to None.
        api_key (str, optional): API KEY. Defaults to Depends(get_api_key).

    Returns:
        dict[str, Any]: dicto of item read
    '''
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item, api_key: str = Depends(get_api_key)) -> dict[str, Any]: # pylint: disable=unused-argument
    '''
    Endpoint to create items

    Args:
        item (Item): Item to create
        api_key (str, optional): API KEY. Defaults to Depends(get_api_key).

    Returns:
        dict[str, Any]: Item created
    '''
    return {"name": item.name, "price": item.price}
