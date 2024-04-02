from fastapi import FastAPI

from auth.auth_router import router as jwt_router
from auth.core.config import settings
from routers.exercise_router import router as exercises_router
from routers.pairs_router import router as pairs_router
from routers.training_router import router as training_router
from routers.user_router import router as user_router

app = FastAPI()
app.include_router(exercises_router)
app.include_router(training_router)
app.include_router(user_router)
app.include_router(pairs_router)
app.include_router(jwt_router, prefix=settings.api_v1_prefix)
