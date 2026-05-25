# --- ЧАСТЬ 1: Импорты ---
from app.api.auth import router as auth_router
from fastapi import FastAPI
# --- ЧАСТЬ 2: Создание приложения ---
app = FastAPI(title="Sheber API")

# --- ЧАСТЬ 3: Подключение маршрутов ---
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# --- ЧАСТЬ 4: Остальной код (твои функции) ---
@app.get("/")
async def root():
    return {"message": "API работает"}