from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_tables, delete_tables
from app.users.router import router as users_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    # await delete_tables()
    # print("Таблицы очищены")
    await create_tables()
    print("Таблицы созданы")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message" : "Домашняя страница"}