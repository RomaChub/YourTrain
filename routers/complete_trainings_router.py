from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel
from sqlalchemy import Integer

from auth.auth_repository import AuthRepository
from chemas.STraining import STrainingId
from chemas.SUser import SUser
from repositories.complete_trainings_repository import CompleteTrainingsRepository

router = APIRouter(
    prefix="/YourTrain",
    tags=['CompleteTrainings']
)


@router.post("/complete-training/start/")
async def start_training(
        training_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
):
    user_id = user.id
    if user.training_start_flag:
        raise HTTPException(status_code=400, detail="You are not allowed to start a training")
    else:
        start_time = datetime.now()
        result_id = await CompleteTrainingsRepository.add_start_time(start_time, training_id, user_id)
        return {"result_id": result_id}


@router.post("/complete-training/end/")
async def end_training(
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
):
    user_id = user.id
    if not user.training_start_flag:
        raise HTTPException(status_code=400, detail="You are not allowed to end a training")
    else:
        end_time = datetime.now()
        result_id = await CompleteTrainingsRepository.add_end_time(end_time, user_id)
        return {"success": True}


@router.get("/complete-trainings/")
async def get_all_completed_trainings():
    completed_trainings = await CompleteTrainingsRepository.get_all_completed_trainings()
    if not completed_trainings:
        raise HTTPException(status_code=404, detail="No completed trainings found")
    return completed_trainings
