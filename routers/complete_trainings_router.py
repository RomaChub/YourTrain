from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel

from auth.auth_repository import AuthRepository
from chemas.SUser import SUser
from repositories.complete_trainings_repository import CompleteTrainingsRepository
from chemas.SCompleteTraining import SCompleteTraining


router = APIRouter(
    prefix="/your_train",
    tags=['CompleteTrainings']
)

class TrainingStartResponse(BaseModel):
    result_id: int

class TrainingEndResponse(BaseModel):
    success: bool

@router.post("/complete-training/start/", response_model=TrainingStartResponse)
async def start_training(
        training_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> TrainingStartResponse:
    user_id = user.id
    if user.training_start_flag:
        raise HTTPException(status_code=400, detail="You are not allowed to start a training")
    else:
        start_time = datetime.now()
        result_id = await CompleteTrainingsRepository.add_start_time(start_time, training_id, user_id)
        return TrainingStartResponse(result_id=result_id)


@router.post("/complete-training/end/", response_model=TrainingEndResponse)
async def end_training(
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> TrainingEndResponse:
    user_id = user.id
    if not user.training_start_flag:
        raise HTTPException(status_code=400, detail="You are not allowed to end a training")
    else:
        end_time = datetime.now()
        result_id = await CompleteTrainingsRepository.add_end_time(end_time, user_id)
        return TrainingEndResponse(success=True)


@router.get("/complete-trainings/", response_model=List[SCompleteTraining])
async def get_all_completed_trainings() -> List[SCompleteTraining]:
    completed_trainings = await CompleteTrainingsRepository.get_all_completed_trainings()
    if not completed_trainings:
        raise HTTPException(status_code=404, detail="No completed trainings found")
    return completed_trainings
