from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth_repository import AuthRepository
from auth.schemas import UserSchema
from repositories.training_repository import TrainingRepository
from chemas.schemas import STrainingAdd, STraining, STrainingId

router = APIRouter(
    prefix="/YourTrain",
    tags=['Training']
)


@router.post("/training")
async def add_training(
        training: Annotated[STrainingAdd, Depends()],
        user: UserSchema = Depends(AuthRepository.get_current_active_auth_user),
) -> STrainingId:
    training_id = await TrainingRepository.add_training(training, user.username)
    return {"training_id": training_id}


@router.get("/training/{training_id}")
async def get_one_training(training_id: int):
    training_one = await TrainingRepository.get_one(training_id)
    return training_one


@router.delete("/training/{training_id}")
async def delete_training(training_id: int):
    await TrainingRepository.delete_training(training_id)
    return {"message": f"Training with id {training_id} has been deleted"}


@router.get("/training")
async def get_training() -> list[STraining]:
    training = await TrainingRepository.get_all()
    return training


@router.put("/training/{training_id}")
async def update_training(training_id: int, name: str, exercises: int):
    success = await TrainingRepository.update_training(training_id, name, exercises)
    return {"message": f"Training {training_id} updated successfully"}
