from fastapi import FastAPI

from contextlib import asynccontextmanager
from database.database import create_tables, delete_tables
from routers.exercise import router as exercises_router
from routers.training import router as training_router
from routers.user import router as user_router
from routers.pairs import router as pairs_router
from auth.core.config import settings
from auth.auth_router import router as jwt_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Db ready")
    yield
    print("Off")


app = FastAPI(lifespan=lifespan)
app.include_router(exercises_router)
app.include_router(training_router)
app.include_router(user_router)
app.include_router(pairs_router)
app.include_router(jwt_router, prefix=settings.api_v1_prefix)
