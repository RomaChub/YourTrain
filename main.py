from fastapi import FastAPI

from contextlib import asynccontextmanager

from routers.exercise import router as exercises_router
from routers.training import router as training_router
from routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Db ready")
    yield
    print("Off")


app = FastAPI(lifespan=lifespan)
app.include_router(exercises_router)
app.include_router(training_router)
app.include_router(user_router)