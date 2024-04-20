from fastapi import FastAPI

from api.auth.auth_router import router as jwt_router
from api.auth.core.config import settings
from api.routers.exercise_router import router as exercises_router
from api.routers.pairs_router import router as pairs_router
from api.routers.training_router import router as training_router
from api.routers.user_router import router as user_router
from api.routers.complete_trainings_router import router as complete_trainings_router
from api.routers.images_router import router as images_router

app = FastAPI()
app.include_router(exercises_router)
app.include_router(training_router)
app.include_router(user_router)
app.include_router(pairs_router)
app.include_router(jwt_router, prefix=settings.api_v1_prefix)
app.include_router(complete_trainings_router)
app.include_router(images_router)
