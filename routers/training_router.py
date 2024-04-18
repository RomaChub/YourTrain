from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from auth.auth_repository import AuthRepository
from chemas import SUser
from repositories.training_repository import TrainingRepository
from chemas.STraining import STrainingAdd, STraining, STrainingId, SFullTraining

router = APIRouter(
    prefix="/your_train",
    tags=['Training']
)


@router.post("/training", response_model=STrainingId)
async def add_training(
        training: Annotated[STrainingAdd, Depends()],
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> STrainingId:
    try:
        training_id = await TrainingRepository.add_training(training, user.id)
        return {"id": training_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training/{training_id}", response_model=STraining)
async def get_one_training(training_id: int) -> STraining:
    try:
        training_one = await TrainingRepository.get_one(training_id)
        if not training_one:
            raise HTTPException(status_code=404, detail="Training not found")
        return training_one
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training/full/{training_id}", response_model=SFullTraining)
async def get_full_training(training_id: int) -> SFullTraining:
    try:
        training = await TrainingRepository.get_training(training_id)
        if not training:
            raise HTTPException(status_code=404, detail="Training not found")
        return training
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/training/{training_id}", response_model=STrainingId)
async def delete_training(training_id: int) -> STrainingId:
    try:
        await TrainingRepository.delete_training(training_id)
        return {"id": training_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/training", response_model=List[STraining])
async def get_training() -> List[STraining]:
    try:
        training = await TrainingRepository.get_all()
        return training
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/training/{training_id}", response_model=STrainingId)
async def update_training(training_id: int, name: Annotated[STrainingAdd, Depends()]) -> STrainingId:
    try:
        success = await TrainingRepository.update_training(training_id, name)
        if not success:
            raise HTTPException(status_code=404, detail="Training not found")
        return {"id": training_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
