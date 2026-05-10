from fastapi import APIRouter, HTTPException, Path, Query
from app.schemas import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])
fake_db = {}
counter = 0


@router.post(
    "/",
    response_model=Item,
    summary="Создать новый товар",
    description="Создает новый товар в базе данных и возвращает его с присвоенным ID",
    response_description="Созданный товар с уникальным ID",
    responses={
        200: {"description": "Товар успешно создан"},
        422: {"description": "Ошибка валидации данных"}
    }
)
async def create_item(item: ItemCreate):
    """
    Создание нового товара.
    
    - **name**: Название товара
    - **price**: Цена товара
    """
    global counter
    counter += 1
    new_item = Item(id=counter, **item.model_dump())
    fake_db[counter] = new_item
    return new_item


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Получить товар по ID",
    description="Возвращает информацию о товаре по его уникальному идентификатору",
    response_description="Информация о запрошенном товаре",
    responses={
        200: {"description": "Товар найден"},
        404: {"description": "Товар не найден"}
    }
)
async def get_item(
    item_id: int = Path(
        ...,
        title="ID товара",
        description="Уникальный идентификатор товара",
        ge=1,
        example=1
    ),
    q: str = Query(
        None,
        title="Поисковый запрос",
        description="Опциональный поисковый запрос для фильтрации",
        max_length=50
    )
):
    """
    Получение товара по ID с опциональным поисковым запросом.
    
    - **item_id**: Уникальный идентификатор товара
    - **q**: Опциональный поисковый запрос (не влияет на результат)
    """
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]