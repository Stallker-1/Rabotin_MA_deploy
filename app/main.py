from fastapi import FastAPI, Depends, HTTPException
from app.config import Settings
from app.routers import items
import time
import json
import logging
from datetime import datetime

# Настройка структурированного JSON-логирования
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Добавляем exception info если есть
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

# Настройка корневого логгера
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Очищаем существующие хендлеры
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Добавляем JSON хендлер для консоли
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

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

# Время запуска приложения для healthcheck
startup_time = time.time()


@app.get("/", tags=["root"])
async def root():
    """
    Корневой эндпоинт для проверки работы API.
    
    Returns:
        Приветственное сообщение
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Hello, World!",
        "environment": settings.environment,
        "app_name": settings.app_name
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Healthcheck эндпоинт для проверки состояния приложения.
    
    Используется Docker healthcheck для мониторинга.
    
    Returns:
        Статус приложения и время работы
    """
    uptime = time.time() - startup_time
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime, 2),
        "environment": settings.environment,
        "checks": {
            "database": "ok" if settings.database_url else "not_configured",
            "api": "ok"
        }
    }
    
    logger.info(f"Health check performed: {health_status['status']}")
    return health_status