from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router as exercises_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Db clear")
    await create_tables()
    print("Db ready")
    yield
    print("Off")


app = FastAPI(lifespan=lifespan)
app.include_router(exercises_router)
