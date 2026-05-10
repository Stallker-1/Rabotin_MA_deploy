from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(
        title="Название товара",
        description="Название товара должно быть уникальным",
        example="Ноутбук Apple MacBook Pro"
    )
    price: float = Field(
        title="Цена товара",
        description="Цена в рублях",
        example=129999.99,
        gt=0
    )


class Item(ItemCreate):
    id: int = Field(
        title="ID товара",
        description="Уникальный идентификатор товара",
        example=1
    )