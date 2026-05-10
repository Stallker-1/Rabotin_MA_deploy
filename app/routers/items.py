from fastapi import APIRouter, HTTPException
from app.schemas import Item, ItemCreate

router = APIRouter(prefix="/items")
fake_db = {}
counter = 0

@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    global counter
    counter += 1
    new_item = Item(id=counter, **item.dict())
    fake_db[counter] = new_item
    return new_item

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(404, "Item not found")
    return fake_db[item_id]