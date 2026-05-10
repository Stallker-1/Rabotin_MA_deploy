from fastapi import FastAPI
from app.config import Settings
from app.routers import items

settings = Settings()
app = FastAPI(
    title=settings.app_name,
    description="Учебный проект для демонстрации тестирования и деплоя",
    version="1.0.0",
    contact={
        "name": "Иван Иванов",
        "email": "student@example.com"
    },
)

app.include_router(items.router)


@app.get("/", tags=["root"])
async def root():
    """
    Корневой эндпоинт для проверки работы API.
    
    Returns:
        Приветственное сообщение
    """
    return {
        "message": "Hello, World!",
        "environment": settings.environment,
        "app_name": settings.app_name
    }