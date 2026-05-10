from fastapi import FastAPI
from app.config import Settings

settings = Settings()
app = FastAPI(title=settings.app_name)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}