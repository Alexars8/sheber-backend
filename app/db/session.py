from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Создаем движок базы данных
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Будет показывать в терминале сами SQL-запросы (удобно для тестов)
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция-зависимость (Dependency Injection) для получения сессии в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()