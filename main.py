from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, delete_tables, create_tables_training,delete_tables_training
from router import router as exercises_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #await delete_tables()
    #await delete_tables_training()
    #print("Db clear")
    await create_tables()
    await create_tables_training()
    print("Db ready")
    yield
    print("Off")


app = FastAPI(lifespan=lifespan)
app.include_router(exercises_router)
