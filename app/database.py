from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import get_db_url

class Model(DeclarativeBase):
    pass

engine = create_async_engine(
    get_db_url(),
    connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)