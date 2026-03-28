from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)

print(f"подключился к {DATABASE_URL}")