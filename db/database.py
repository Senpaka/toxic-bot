from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import make_url

load_dotenv()

class DatabaseHelper:
    """
    Обертка для удобства подключения к бд
    """
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url,
            echo=echo
        )
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def dispose(self):
        await self.engine.dispose()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

db = DatabaseHelper(DATABASE_URL, True)

async_session = db.async_session

print(f"подключился к {make_url(DATABASE_URL).host}")